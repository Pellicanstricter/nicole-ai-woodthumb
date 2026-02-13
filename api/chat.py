"""
Chat endpoint for website widget
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from .nicole import nicole
import json

router = APIRouter()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []
    stream: bool = True

    class Config:
        # Add validation
        str_max_length = 2000  # Max message length


class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Handle chat widget messages
    Supports streaming and non-streaming responses
    """
    try:
        # Validate input
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        if len(request.message) > 2000:
            raise HTTPException(status_code=400, detail="Message too long (max 2000 characters)")

        if len(request.conversation_history) > 50:
            raise HTTPException(status_code=400, detail="Conversation history too long")

        # Convert Pydantic models to dicts for Nicole
        history = [msg.dict() for msg in request.conversation_history]

        if request.stream:
            # Streaming response
            async def generate():
                # generate_response returns the async generator directly when stream=True
                response_generator = nicole.generate_response(
                    message=request.message,
                    conversation_history=history,
                    stream=True
                )
                async for chunk in response_generator:
                    # Send as Server-Sent Events
                    yield f"data: {json.dumps(chunk)}\n\n"

            return StreamingResponse(
                generate(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        else:
            # Non-streaming response
            result = await nicole.generate_response(
                message=request.message,
                conversation_history=history,
                stream=False
            )
            return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/test")
async def chat_test():
    """Simple test endpoint"""
    return {"status": "ok", "message": "Chat endpoint is working"}
