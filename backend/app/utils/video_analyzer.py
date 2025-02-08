# backend/app/utils/video_analyzer.py
import cv2
import numpy as np
from pathlib import Path
import google.generativeai as genai
import base64
import sys
import os

# Add the parent directory to sys.path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import VIDEO_DIR

class VideoAnalyzer:
    def __init__(self, gemini_api_key: str):
        self.model = genai.GenerativeModel('gemini-pro-vision')
        genai.configure(api_key=gemini_api_key)

    async def save_and_analyze(self, file, dispute_id: str) -> dict:
        filename = f"{dispute_id}_{file.filename}"
        file_path = VIDEO_DIR / filename

        # Save file
        with open(file_path, "wb") as video_file:
            content = await file.read()
            video_file.write(content)

        return await self.analyze_video(file_path)

    async def analyze_video(self, file_path: Path) -> dict:
        cap = cv2.VideoCapture(str(file_path))
        frames = self._extract_key_frames(cap)
        
        # Convert frames to base64 for Gemini API
        encoded_frames = self._encode_frames(frames)
        
        # Analyze with Gemini AI
        prompt = self._generate_analysis_prompt()
        response = await self.model.generate_content([prompt, encoded_frames])
        
        return self._parse_analysis_response(response.text)

    def _extract_key_frames(self, cap, max_frames=5):
        frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = total_frames // max_frames

        for i in range(0, total_frames, interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)

        cap.release()
        return frames[:max_frames]

    def _encode_frames(self, frames):
        encoded_images = []
        for frame in frames:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Encode frame to jpg
            _, buffer = cv2.imencode('.jpg', rgb_frame)
            
            # Convert to base64
            base64_frame = base64.b64encode(buffer).decode('utf-8')
            encoded_images.append({
                'mime_type': 'image/jpeg',
                'data': base64_frame
            })
        
        return encoded_images

    def _generate_analysis_prompt(self) -> str:
        return """
        Analyze these video frames for authenticity:
        1. Check if the interface matches the official app
        2. Verify transaction details visibility
        3. Check for video manipulation signs
        4. Verify natural interaction patterns

        Provide analysis in JSON format:
        {
            "authenticity_score": float (0-100),
            "interface_valid": boolean,
            "interaction_natural": boolean,
            "manipulation_detected": boolean,
            "risk_factors": [string]
        }
        """

    def _parse_analysis_response(self, response: str) -> dict:
        try:
            analysis = eval(response)
            return {
                "authenticity_score": analysis["authenticity_score"],
                "interface_valid": analysis["interface_valid"],
                "interaction_natural": analysis["interaction_natural"],
                "manipulation_detected": analysis["manipulation_detected"],
                "risk_factors": analysis["risk_factors"]
            }
        except Exception as e:
            return {
                "error": f"Failed to parse analysis: {str(e)}",
                "authenticity_score": 0,
                "interface_valid": False,
                "interaction_natural": False,
                "manipulation_detected": True,
                "risk_factors": ["Analysis parsing failed"]
            }

# Add test code if running directly
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    async def test_analyzer():
        analyzer = VideoAnalyzer(os.getenv("GEMINI_API_KEY"))
        # Add test code here
        print("Video analyzer initialized successfully")
        
    # Run the test
    asyncio.run(test_analyzer())