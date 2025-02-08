# backend/app/mock_data.py

import os
from datetime import datetime, timedelta
from pathlib import Path
from utils.pdf_analyzer import PDFAnalyzer
from utils.video_analyzer import VideoAnalyzer
from risk_analyzer import RiskAnalyzer
from dotenv import load_dotenv

load_dotenv()

# Initialize analyzers
pdf_analyzer = PDFAnalyzer(os.getenv("GEMINI_API_KEY"))
video_analyzer = VideoAnalyzer(os.getenv("GEMINI_API_KEY"))
risk_analyzer = RiskAnalyzer()

async def generate_mock_disputes():
    # Sample PDF and video files from storage
    pdf_path = Path("app/storage/evidence_pdfs/Lloyds-Bank-Statement-TemplateLab.com_.pdf")
    
    # Generate real analysis results
    pdf_analysis = await pdf_analyzer.analyze_pdf(pdf_path)
    
    # Since we can't store video in git, we'll use the analyzer's logic without actual file
    video_analysis = {
        "authenticity_score": 92.5,
        "interface_valid": True,
        "interaction_natural": True,
        "manipulation_detected": False,
        "risk_factors": []
    }

    # Base risk calculation data
    base_risk_data = {
        'amount': 1500.00,
        'patterns': ['multiple attempts', 'unusual location'],
        'evidence_list': [
            {
                'type': 'bank_statement',
                'verified': True,
                'quality': 'high'
            },
            {
                'type': 'video_recording',
                'quality': 'high'
            }
        ]
    }

    # Calculate risk scores using actual risk analyzer
    risk_assessment = risk_analyzer.calculate_risk_score(base_risk_data)

    return [
        {
            "id": "D123456",
            "type": "Unauthorized Transaction",
            "amount": 1500.00,
            "status": risk_assessment['status'],
            "createdAt": datetime.now().isoformat(),
            "timeRemaining": "1h 45m",
            "riskScore": risk_assessment['risk_score'],
            "buyer": {
                "username": "john_doe",
                "riskScore": "Low",
                "verifiedStatus": True,
                "accountAge": "2 years",
                "previousDisputes": 1
            },
            "seller": {
                "username": "tech_store",
                "riskScore": "Low",
                "verifiedStatus": True,
                "accountAge": "3 years",
                "previousDisputes": 2
            },
            "evidence": {
                "bank_statement": {
                    "authenticity_score": pdf_analysis["authenticity_score"],
                    "metadata_valid": pdf_analysis["metadata_valid"],
                    "content_match": pdf_analysis["content_match"],
                    "suspicious_patterns": pdf_analysis["suspicious_patterns"]
                },
                "video_evidence": video_analysis
            }
        },
        {
            "id": "D123457",
            "type": "Non-receipt of Goods",
            "amount": 2500.00,
            # Modify risk data for different scenario
            "status": risk_analyzer.calculate_risk_score({**base_risk_data, 'amount': 2500.00})['status'],
            "createdAt": (datetime.now() - timedelta(hours=1)).isoformat(),
            "timeRemaining": "2h 15m",
            "riskScore": risk_analyzer.calculate_risk_score({**base_risk_data, 'amount': 2500.00})['risk_score'],
            "buyer": {
                "username": "alice_smith",
                "riskScore": "Medium",
                "verifiedStatus": True,
                "accountAge": "6 months",
                "previousDisputes": 2
            },
            "seller": {
                "username": "electronics_hub",
                "riskScore": "Low",
                "verifiedStatus": True,
                "accountAge": "1 year",
                "previousDisputes": 1
            },
            "evidence": {
                "bank_statement": {
                    "authenticity_score": pdf_analysis["authenticity_score"] - 7,  # Slightly lower score
                    "metadata_valid": pdf_analysis["metadata_valid"],
                    "content_match": pdf_analysis["content_match"],
                    "suspicious_patterns": ["Unusual transaction time"]
                }
            }
        },
        {
            "id": "D123458",
            "type": "Incorrect Amount",
            "amount": 750.00,
            # Lower risk scenario
            "status": risk_analyzer.calculate_risk_score({**base_risk_data, 'amount': 750.00, 'patterns': []})['status'],
            "createdAt": (datetime.now() - timedelta(hours=2)).isoformat(),
            "resolvedAt": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "timeRemaining": "0h 0m",
            "riskScore": risk_analyzer.calculate_risk_score({**base_risk_data, 'amount': 750.00, 'patterns': []})['risk_score'],
            "resolution": "Refunded",
            "resolutionConfidence": 98,
            "buyer": {
                "username": "mary_johnson",
                "riskScore": "Low",
                "verifiedStatus": True,
                "accountAge": "1.5 years",
                "previousDisputes": 0
            },
            "seller": {
                "username": "fashion_store",
                "riskScore": "Low",
                "verifiedStatus": True,
                "accountAge": "2 years",
                "previousDisputes": 1
            },
            "evidence": {
                "bank_statement": {
                    "authenticity_score": pdf_analysis["authenticity_score"] + 3,  # Higher score
                    "metadata_valid": True,
                    "content_match": True,
                    "suspicious_patterns": []
                },
                "video_evidence": {
                    **video_analysis,
                    "authenticity_score": 96  # Higher score for resolved case
                }
            }
        },
        {
            "id": "D123459",
            "type": "Double Charge",
            "amount": 1200.00,
            # Medium risk scenario
            "status": risk_analyzer.calculate_risk_score({
                **base_risk_data, 
                'amount': 1200.00, 
                'patterns': ['multiple attempts']
            })['status'],
            "createdAt": (datetime.now() - timedelta(hours=3)).isoformat(),
            "timeRemaining": "3h 30m",
            "riskScore": risk_analyzer.calculate_risk_score({
                **base_risk_data, 
                'amount': 1200.00, 
                'patterns': ['multiple attempts']
            })['risk_score'],
            "buyer": {
                "username": "peter_wilson",
                "riskScore": "Medium",
                "verifiedStatus": False,
                "accountAge": "3 months",
                "previousDisputes": 3
            },
            "seller": {
                "username": "digital_goods",
                "riskScore": "Medium",
                "verifiedStatus": True,
                "accountAge": "8 months",
                "previousDisputes": 2
            },
            "evidence": {
                "bank_statement": {
                    "authenticity_score": pdf_analysis["authenticity_score"] - 10,
                    "metadata_valid": True,
                    "content_match": True,
                    "suspicious_patterns": ["Multiple attempts"]
                }
            }
        },
        {
            "id": "D123460",
            "type": "Service Not Provided",
            "amount": 3000.00,
            # High risk scenario
            "status": risk_analyzer.calculate_risk_score({
                **base_risk_data, 
                'amount': 3000.00, 
                'patterns': ['unusual location', 'multiple devices']
            })['status'],
            "createdAt": (datetime.now() - timedelta(hours=4)).isoformat(),
            "timeRemaining": "4h 15m",
            "riskScore": risk_analyzer.calculate_risk_score({
                **base_risk_data, 
                'amount': 3000.00, 
                'patterns': ['unusual location', 'multiple devices']
            })['risk_score'],
            "buyer": {
                "username": "sarah_brown",
                "riskScore": "High",
                "verifiedStatus": False,
                "accountAge": "1 month",
                "previousDisputes": 4
            },
            "seller": {
                "username": "service_provider",
                "riskScore": "Medium",
                "verifiedStatus": True,
                "accountAge": "6 months",
                "previousDisputes": 3
            },
            "evidence": {
                "bank_statement": {
                    "authenticity_score": pdf_analysis["authenticity_score"] - 20,
                    "metadata_valid": True,
                    "content_match": False,
                    "suspicious_patterns": ["Unusual location", "Multiple devices"]
                },
                "video_evidence": {
                    "authenticity_score": 82,
                    "interface_valid": True,
                    "interaction_natural": False,
                    "manipulation_detected": True,
                    "risk_factors": ["Suspicious interaction patterns"]
                }
            }
        }
    ]

# Update main.py to use this generator
async def generate_mock_disputes():
    # Remove the file dependency
    mock_pdf_analysis = {
        "authenticity_score": 92.5,
        "metadata_valid": True,
        "content_match": True,
        "suspicious_patterns": []
    }
    
    mock_video_analysis = {
        "authenticity_score": 92.5,
        "interface_valid": True,
        "interaction_natural": True,
        "manipulation_detected": False,
        "risk_factors": []
    }

    # Base risk calculation data
    base_risk_data = {
        'amount': 1500.00,
        'patterns': ['multiple attempts', 'unusual location'],
        'evidence_list': [
            {
                'type': 'bank_statement',
                'verified': True,
                'quality': 'high'
            },
            {
                'type': 'video_recording',
                'quality': 'high'
            }
        ]
    }

    try:
        return MOCK_DISPUTES  # Use the static mock data instead
    except Exception as e:
        print(f"Error generating mock disputes: {str(e)}")
        return []