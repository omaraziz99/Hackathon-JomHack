from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Mock data for disputes
MOCK_DISPUTES = [
    {
        "id": "D123456",
        "type": "Unauthorized Transaction",
        "amount": 1500.00,
        "status": "High Risk",
        "createdAt": datetime.now().isoformat(),
        "timeRemaining": "1h 45m",
        "riskScore": 85,
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
                "authenticity_score": 92.5,
                "metadata_valid": True,
                "content_match": True,
                "suspicious_patterns": []
            },
            "video_evidence": {
                "authenticity_score": 92.5,
                "interface_valid": True,
                "interaction_natural": True,
                "manipulation_detected": False,
                "risk_factors": []
            }
        }
    }
]

# Models
class Dispute(BaseModel):
    id: str
    type: str
    amount: float
    status: str
    createdAt: str
    timeRemaining: str
    riskScore: int
    buyer: dict
    seller: dict
    evidence: dict

# Endpoints
@app.get("/disputes/active", response_model=List[Dispute])
async def get_active_disputes():
    return [d for d in MOCK_DISPUTES if "resolvedAt" not in d]

@app.get("/disputes/ai-resolved", response_model=List[Dispute])
async def get_ai_resolved_disputes():
    return [d for d in MOCK_DISPUTES if "resolvedAt" in d]

@app.get("/disputes/active-metrics")
async def get_active_metrics():
    return {
        "activeDisputes": len([d for d in MOCK_DISPUTES if "resolvedAt" not in d]),
        "avgResolutionTime": "1.5h",
        "resolvedToday": 18,
        "fraudPrevented": "$2.4k"
    }

@app.get("/disputes/ai-metrics")
async def get_ai_metrics():
    return {
        "aiResolutions": 156,
        "avgAiResolutionTime": "45s",
        "successRate": "98%",
        "costSaved": "$5.2k"
    }

@app.get("/disputes/active/{dispute_id}", response_model=Dispute)
async def get_active_dispute_details(dispute_id: str):
    dispute = next((d for d in MOCK_DISPUTES if d["id"] == dispute_id and "resolvedAt" not in d), None)
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    return dispute

@app.get("/disputes/ai/{dispute_id}", response_model=Dispute)
async def get_ai_dispute_details(dispute_id: str):
    dispute = next((d for d in MOCK_DISPUTES if d["id"] == dispute_id and "resolvedAt" in d), None)
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    return dispute

@app.get("/disputes/{dispute_id}/evidence")
async def get_dispute_evidence(dispute_id: str):
    dispute = next((d for d in MOCK_DISPUTES if d["id"] == dispute_id), None)
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    return dispute["evidence"]