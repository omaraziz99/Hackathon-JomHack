# backend/app/models.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class EvidenceAnalysis(BaseModel):
    authenticity_score: float
    metadata_valid: bool
    content_match: bool
    timestamp_valid: bool
    risk_factors: List[str]

class VideoAnalysis(BaseModel):
    authenticity_score: float
    interface_valid: bool
    interaction_natural: bool
    manipulation_detected: bool
    risk_factors: List[str]

class DisputeEvidence(BaseModel):
    dispute_id: str
    evidence_type: str
    file_path: str
    uploaded_at: datetime
    analysis_result: Optional[dict]

class DisputeAnalysis(BaseModel):
    case_id: str
    risk_score: float
    evidence_score: float
    fraud_indicators: List[str]
    recommendation: str