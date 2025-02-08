# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict
from datetime import datetime
from app.utils.pdf_analyzer import PDFAnalyzer
from app.utils.video_analyzer import VideoAnalyzer
from app.risk_analyzer import RiskAnalyzer
from app.models import DisputeAnalysis
import os
from dotenv import load_dotenv
from app.mock_data import get_mock_disputes
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pdf_analyzer = PDFAnalyzer(os.getenv("GEMINI_API_KEY"))
video_analyzer = VideoAnalyzer(os.getenv("GEMINI_API_KEY"))
risk_analyzer = RiskAnalyzer()

@app.get("/api/disputes")
async def get_disputes(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    try:
        disputes = MOCK_DISPUTES  # Use static mock data directly
        
        # Filter by status if provided
        if status:
            if status == "resolved":
                disputes = [d for d in disputes if d.get("resolvedAt")]
            else:
                disputes = [d for d in disputes if not d.get("resolvedAt")]
        
        # Pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_disputes = disputes[start_idx:end_idx]
        
        return {
            "data": paginated_disputes,
            "total": len(disputes),
            "page": page,
            "total_pages": (len(disputes) + limit - 1) // limit
        }
    except Exception as e:
        print(f"Error in get_disputes: {str(e)}")
        return {
            "data": [],
            "total": 0,
            "page": 1,
            "total_pages": 0
        }
    
@app.get("/api/disputes")
async def get_disputes(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    try:
        disputes = await get_mock_disputes()
        
        # Filter by status if provided
        if status:
            if status == "resolved":
                disputes = [d for d in disputes if d.get("resolvedAt")]
            else:
                disputes = [d for d in disputes if not d.get("resolvedAt")]
        
        # Pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_disputes = disputes[start_idx:end_idx]
        
        return {
            "data": paginated_disputes,
            "total": len(disputes),
            "page": page,
            "total_pages": (len(disputes) + limit - 1) // limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/disputes")
async def get_disputes(
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    disputes = await get_mock_disputes()
    
    if status:
        disputes = [d for d in disputes if d["status"] == status]
    
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    return {
        "data": disputes[start_idx:end_idx],
        "total": len(disputes),
        "page": page,
        "total_pages": (len(disputes) + limit - 1) // limit
    }

@app.get("/api/disputes/{dispute_id}")
async def get_dispute_details(dispute_id: str):
    disputes = await get_mock_disputes()
    dispute = next((d for d in disputes if d["id"] == dispute_id), None)
    
    if not dispute:
        raise HTTPException(status_code=404, detail="Dispute not found")
    
    return dispute

@app.get("/api/disputes", response_model=List[Dict])
async def get_disputes(
    status: Optional[str] = Query(None, description="Filter by dispute status"),
    from_date: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    """
    Get a list of disputes with optional filtering and pagination.
    """
    try:
        # Mock data - replace with actual database query
        disputes = [
            {
                "dispute_id": "D123",
                "customer_id": "C456",
                "status": "pending",
                "submission_date": "2024-02-20",
                "amount": 1500.00,
                "risk_score": 85.5,
                "evidence_status": {
                    "bank_statement": True,
                    "video_evidence": True
                }
            },
            {
                "dispute_id": "D124",
                "customer_id": "C457",
                "status": "reviewed",
                "submission_date": "2024-02-21",
                "amount": 2500.00,
                "risk_score": 92.0,
                "evidence_status": {
                    "bank_statement": True,
                    "video_evidence": False
                }
            }
        ]

        # Apply filters
        if status:
            disputes = [d for d in disputes if d["status"] == status]
        
        if from_date:
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
            disputes = [d for d in disputes if datetime.strptime(d["submission_date"], "%Y-%m-%d") >= from_date]
        
        if to_date:
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
            disputes = [d for d in disputes if datetime.strptime(d["submission_date"], "%Y-%m-%d") <= to_date]

        # Calculate pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_disputes = disputes[start_idx:end_idx]

        return {
            "data": paginated_disputes,
            "total": len(disputes),
            "page": page,
            "total_pages": (len(disputes) + limit - 1) // limit
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/disputes/{dispute_id}", response_model=Dict)
async def get_dispute_details(
    dispute_id: str = Path(..., description="The ID of the dispute to retrieve")
):
    """
    Get detailed information about a specific dispute.
    """
    try:
        # Mock data - replace with actual database query
        dispute_details = {
            "dispute_id": dispute_id,
            "customer_id": "C456",
            "status": "pending",
            "submission_date": "2024-02-20",
            "amount": 1500.00,
            "risk_score": 85.5,
            "evidence_analysis": {
                "pdf_analysis": {
                    "authenticity_score": 85.5,
                    "metadata_valid": True,
                    "content_match": True,
                    "suspicious_patterns": [],
                    "recommendation": "Document appears authentic"
                },
                "video_analysis": {
                    "authenticity_score": 90.0,
                    "interface_valid": True,
                    "interaction_natural": True,
                    "manipulation_detected": False,
                    "risk_factors": []
                },
                "overall_assessment": {
                    "risk_level": "low",
                    "confidence_score": 87.75,
                    "recommendations": ["Proceed with dispute resolution"]
                }
            },
            "timeline": [
                {
                    "timestamp": "2024-02-20T10:00:00Z",
                    "event": "Dispute submitted",
                    "details": "Customer submitted dispute with evidence"
                },
                {
                    "timestamp": "2024-02-20T10:05:00Z",
                    "event": "Evidence analyzed",
                    "details": "Automated analysis completed"
                }
            ]
        }

        if not dispute_details:
            raise HTTPException(status_code=404, detail="Dispute not found")

        return dispute_details

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/summary")
async def get_analytics_summary():
    """
    Get summary analytics for disputes and evidence analysis.
    """
    try:
        # Mock data - replace with actual analytics calculations
        return {
            "total_disputes": 150,
            "risk_distribution": {
                "high": 15,
                "medium": 45,
                "low": 90
            },
            "average_processing_time": "2.5 hours",
            "evidence_stats": {
                "total_analyzed": 300,
                "average_authenticity_score": 88.5,
                "suspicious_cases": 25
            },
            "trending_patterns": [
                {
                    "pattern": "Multiple small transactions",
                    "occurrence": 35
                },
                {
                    "pattern": "International transactions",
                    "occurrence": 28
                }
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/evidence/{dispute_id}/files")
async def get_evidence_files(
    dispute_id: str = Path(..., description="The ID of the dispute")
):
    """
    Get information about evidence files associated with a dispute.
    """
    try:
        # Mock data - replace with actual file system/database query
        return {
            "dispute_id": dispute_id,
            "files": [
                {
                    "type": "bank_statement",
                    "filename": f"{dispute_id}_statement.pdf",
                    "upload_date": "2024-02-20T10:00:00Z",
                    "file_size": 1024576,
                    "analysis_status": "completed"
                },
                {
                    "type": "video_evidence",
                    "filename": f"{dispute_id}_recording.mp4",
                    "upload_date": "2024-02-20T10:00:00Z",
                    "file_size": 5242880,
                    "analysis_status": "completed"
                }
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/evidence/upload")
async def upload_evidence(
    dispute_id: str,
    bank_statement: UploadFile = File(...),
    video_evidence: UploadFile = File(...)
):
    try:
        # Analyze both pieces of evidence
        pdf_analysis = await pdf_analyzer.save_and_analyze(bank_statement, dispute_id)
        video_analysis = await video_analyzer.save_and_analyze(video_evidence, dispute_id)

        # Combine analyses for risk assessment
        evidence_data = {
            "pdf_score": pdf_analysis["authenticity_score"],
            "video_score": video_analysis["authenticity_score"],
            "suspicious_patterns": pdf_analysis.get("suspicious_patterns", []),
            "risk_factors": video_analysis.get("risk_factors", [])
        }

        # Calculate overall risk score
        risk_score = risk_analyzer.calculate_risk_score(evidence_data)

        return {
            "status": "success",
            "pdf_analysis": pdf_analysis,
            "video_analysis": video_analysis,
            "risk_assessment": risk_score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/risk-analysis/summary")
async def get_risk_analysis_summary() -> Dict:
    """
    Get risk analysis summary based on existing dispute data
    """
    # Sample dispute data for demonstration
    sample_data = {
        'amount': 750,
        'patterns': ['multiple attempts', 'unusual location'],
        'evidence_list': [
            {
                'type': 'bank_statement',
                'verified': True
            },
            {
                'type': 'video_recording',
                'quality': 'high'
            }
        ]
    }

    # Get risk analysis using existing method
    risk_assessment = risk_analyzer.calculate_risk_score(sample_data)

    # Format the response
    return {
        "risk_assessment": {
            "risk_score": risk_assessment['risk_score'],
            "status": risk_assessment['status'],
            "evidence_score": risk_assessment['evidence_score'],
            "contributing_factors": risk_assessment['contributing_factors']
        },
        "analysis_timestamp": datetime.now().isoformat(),
        "model_version": "1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)