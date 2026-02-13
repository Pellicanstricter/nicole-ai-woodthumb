"""
Email endpoint for Gmail integration
Called by Google Apps Script
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from .nicole import nicole

router = APIRouter()


class EmailRequest(BaseModel):
    from_email: EmailStr
    subject: str
    body: str
    thread_id: str = ""


class EmailResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    routing: str  # 'auto_send', 'draft', or 'flag'
    reasoning: str


@router.post("/email", response_model=EmailResponse)
async def process_email(request: EmailRequest):
    """
    Process incoming email and generate response with routing decision

    Called by Google Apps Script every 5 minutes
    Returns response + routing decision (auto-send, draft, or flag)
    """
    try:
        result = await nicole.generate_email_response(
            subject=request.subject,
            body=request.body,
            from_email=request.from_email
        )

        return EmailResponse(
            response=result["response"],
            intent=result["intent"],
            confidence=result["confidence"],
            routing=result["routing"],
            reasoning=result["reasoning"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/email/test")
async def email_test():
    """Simple test endpoint"""
    return {"status": "ok", "message": "Email endpoint is working"}
