
# backend/app/utils/pdf_analyzer.py
import fitz  # PyMuPDF
from pathlib import Path
import google.generativeai as genai
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PDF_DIR

class PDFAnalyzer:
    def __init__(self, gemini_api_key: str):
        self.model = genai.GenerativeModel('gemini-pro-vision')
        genai.configure(api_key=gemini_api_key)

    async def save_and_analyze(self, file, dispute_id: str) -> dict:
        # Generate unique filename
        filename = f"{dispute_id}_{file.filename}"
        file_path = PDF_DIR / filename

        # Save file
        with open(file_path, "wb") as pdf_file:
            content = await file.read()
            pdf_file.write(content)

        return await self.analyze_pdf(file_path)

    async def analyze_pdf(self, file_path: Path) -> dict:
        doc = fitz.open(file_path)
        text_content = ""
        for page in doc:
            text_content += page.get_text()

        # Analyze with Gemini AI
        prompt = self._generate_analysis_prompt(text_content)
        response = await self.model.generate_content(prompt)
        
        return self._parse_analysis_response(response.text)

    def _generate_analysis_prompt(self, content: str) -> str:
        return f"""
        Analyze this bank statement for authenticity:
        {content}

        Provide analysis in JSON format:
        {{
            "authenticity_score": float (0-100),
            "metadata_valid": boolean,
            "content_match": boolean,
            "suspicious_patterns": [string],
            "recommendation": string
        }}
        """

    def _parse_analysis_response(self, response: str) -> dict:
        try:
            analysis = eval(response)
            return {
                "authenticity_score": analysis["authenticity_score"],
                "metadata_valid": analysis["metadata_valid"],
                "content_match": analysis["content_match"],
                "suspicious_patterns": analysis["suspicious_patterns"],
                "recommendation": analysis["recommendation"]
            }
        except Exception as e:
            return {
                "error": f"Failed to parse analysis: {str(e)}",
                "authenticity_score": 0,
                "metadata_valid": False,
                "content_match": False,
                "suspicious_patterns": ["Analysis parsing failed"],
                "recommendation": "Manual review required"
            }