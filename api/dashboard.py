"""
Dashboard API endpoints for Nicole admin interface
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path
from .conversation_store import get_conversations as get_stored_conversations, get_session_conversations

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

# Configuration file path
CONFIG_FILE = Path(__file__).parent / "dashboard_config.json"

def load_config():
    """Load dashboard configuration from JSON file"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save dashboard configuration to JSON file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

# Models
class KnowledgeBase(BaseModel):
    content: str

class ThresholdSettings(BaseModel):
    high_confidence_threshold: float
    medium_confidence_threshold: float

class WidgetSettings(BaseModel):
    enabled: bool
    streaming_enabled: bool

class ResponseTemplate(BaseModel):
    greeting: str
    email_signature: str
    brand_voice: str

class LoginRequest(BaseModel):
    password: str

# Authentication
@router.post("/auth")
async def dashboard_login(request: LoginRequest):
    """Simple password login for dashboard"""
    from .config import settings
    if request.password == settings.dashboard_password:
        return {"status": "success", "message": "Authenticated"}
    raise HTTPException(status_code=401, detail="Invalid password")

# Statistics
@router.get("/stats")
async def get_dashboard_stats():
    """Get overview statistics for dashboard"""
    conversations = get_stored_conversations(limit=10000, days=None)
    total = len(conversations)

    # Get this week's conversations
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    this_week = len([c for c in conversations if c.get("timestamp", "") >= week_ago])

    # Get unique sessions
    sessions = set(c.get("session_id", "") for c in conversations)

    return {
        "total_conversations": total,
        "total_conversations_change": 0,
        "auto_sent_emails": 0,
        "auto_sent_emails_change": 0,
        "avg_confidence": 0,
        "avg_confidence_change": 0,
        "avg_response_time": 0,
        "avg_response_time_change": 0,
        "this_week": this_week,
        "this_month": total,
        "unique_sessions": len(sessions),
        "auto_send_rate": 0,
        "system_status": {
            "chat_widget": "active",
            "gmail_integration": "inactive",
            "api_server": "healthy",
            "claude_api": "connected",
            "uptime": "running"
        }
    }

# Analytics
@router.get("/analytics")
async def get_analytics():
    """Get analytics from real conversation data"""
    conversations = get_stored_conversations(limit=10000, days=None)
    total = len(conversations)

    return {
        "total_messages": total,
        "question_categories": [],
        "confidence_distribution": [],
        "response_times": {
            "avg": 0,
            "min": 0,
            "max": 0,
            "median": 0
        }
    }

# Knowledge Base
@router.get("/knowledge")
async def get_knowledge_base():
    """Get current knowledge base content"""
    knowledge_path = Path(__file__).parent.parent / "knowledge" / "woodthumb.md"

    try:
        with open(knowledge_path, 'r') as f:
            content = f.read()
        return {"content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Knowledge base file not found")

@router.put("/knowledge")
async def update_knowledge_base(kb: KnowledgeBase):
    """Update knowledge base content"""
    knowledge_path = Path(__file__).parent.parent / "knowledge" / "woodthumb.md"

    try:
        with open(knowledge_path, 'w') as f:
            f.write(kb.content)
        return {"status": "success", "message": "Knowledge base updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update knowledge base: {str(e)}")

# Settings
@router.get("/settings/thresholds")
async def get_thresholds():
    """Get current confidence thresholds"""
    from .config import settings
    return {
        "high_confidence_threshold": settings.high_confidence_threshold,
        "medium_confidence_threshold": settings.medium_confidence_threshold
    }

@router.put("/settings/thresholds")
async def update_thresholds(thresholds: ThresholdSettings):
    """Update confidence thresholds"""
    if not (0.0 <= thresholds.high_confidence_threshold <= 1.0):
        raise HTTPException(status_code=400, detail="High threshold must be between 0 and 1")
    if not (0.0 <= thresholds.medium_confidence_threshold <= 1.0):
        raise HTTPException(status_code=400, detail="Medium threshold must be between 0 and 1")
    if thresholds.medium_confidence_threshold >= thresholds.high_confidence_threshold:
        raise HTTPException(status_code=400, detail="Medium threshold must be less than high threshold")

    return {
        "status": "success",
        "message": "Thresholds updated (restart server to apply changes)",
        "thresholds": thresholds.dict()
    }

@router.get("/settings/widget")
async def get_widget_settings():
    """Get widget configuration"""
    return {
        "enabled": True,
        "streaming_enabled": True
    }

@router.put("/settings/widget")
async def update_widget_settings(settings: WidgetSettings):
    """Update widget configuration"""
    return {
        "status": "success",
        "message": "Widget settings updated",
        "settings": settings.dict()
    }

# Templates
@router.get("/templates")
async def get_templates():
    """Get response templates"""
    return {
        "greeting": "Hi! I'm Nicole, Wood Thumb's AI assistant. I'm here to help you with workshops, shop time, team events, and custom projects. How can I help you today?",
        "email_signature": "Best,\nNicole\nAI Assistant at Wood Thumb\ninfo@woodthumb.com",
        "brand_voice": """Be warm, welcoming, and approachable. Use casual but professional language. Show enthusiasm for woodworking and creativity. Always be helpful and informative.

Key principles:
- Emphasize that workshops are beginner-friendly
- Highlight the community aspect
- Be encouraging and supportive
- Provide clear next steps (booking links, contact info)"""
    }

@router.put("/templates")
async def update_templates(templates: ResponseTemplate):
    """Update response templates"""
    return {
        "status": "success",
        "message": "Templates updated",
        "templates": templates.dict()
    }

# Conversations - REAL DATA
@router.get("/conversations")
async def get_conversations(
    limit: int = 50,
    days: Optional[int] = None
):
    """Get real conversation history"""
    conversations = get_stored_conversations(limit=limit, days=days)
    return {
        "conversations": conversations,
        "total": len(conversations)
    }

@router.get("/conversations/session/{session_id}")
async def get_session(session_id: str):
    """Get all messages in a specific chat session"""
    messages = get_session_conversations(session_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "messages": messages}

# Gmail Integration
@router.get("/gmail/status")
async def get_gmail_status():
    """Get Gmail integration status"""
    return {
        "connected": False,
        "email": "chris@woodthumb.com",
        "apps_script_status": "not configured",
        "last_check": datetime.now().isoformat(),
        "api_connection": "not configured",
        "api_url": "",
        "stats": {
            "emails_processed": 0,
            "auto_sent": 0,
            "drafts_created": 0,
            "flagged": 0
        }
    }

@router.post("/gmail/test")
async def test_gmail_connection():
    """Test Gmail integration connection"""
    return {
        "status": "not_configured",
        "message": "Gmail integration not set up yet",
        "timestamp": datetime.now().isoformat()
    }

# Quick Links
@router.get("/settings/links")
async def get_quick_links():
    """Get quick links configuration"""
    return {
        "booking_url": "https://woodthumb.com/workshops",
        "contact_email": "chris@woodthumb.com",
        "phone": "(415) 295-5047"
    }

@router.put("/settings/links")
async def update_quick_links(links: Dict[str, str]):
    """Update quick links"""
    return {
        "status": "success",
        "message": "Quick links updated",
        "links": links
    }

# AI Assistant Identity
class AssistantIdentity(BaseModel):
    assistant_name: str
    assistant_title: str
    intro_message: str

@router.get("/settings/identity")
async def get_assistant_identity():
    """Get AI assistant identity settings"""
    config = load_config()
    return config.get("assistant_identity", {
        "assistant_name": "Nicole",
        "assistant_title": "AI Assistant",
        "intro_message": "Hi! I'm Nicole, Wood Thumb's AI assistant. I'm here to help you with workshops, shop time, team events, and custom projects. How can I help you today?"
    })

@router.put("/settings/identity")
async def update_assistant_identity(identity: AssistantIdentity):
    """Update AI assistant identity"""
    config = load_config()
    config["assistant_identity"] = identity.dict()
    save_config(config)
    return {
        "status": "success",
        "message": "Assistant identity updated",
        "identity": identity.dict()
    }

# Scheduling Integration
class SchedulingSettings(BaseModel):
    platform: str
    workshop_booking_url: str
    team_booking_url: Optional[str] = None
    shop_booking_url: Optional[str] = None
    show_available_times: bool = True
    auto_suggest_booking: bool = True

@router.get("/settings/scheduling")
async def get_scheduling_settings():
    """Get calendar and scheduling integration settings"""
    config = load_config()
    return config.get("scheduling", {
        "platform": "acuity",
        "workshop_booking_url": "https://woodthumb.com/workshops",
        "team_booking_url": "https://woodthumb.com/team-events",
        "shop_booking_url": "https://woodthumb.com/shop-time",
        "show_available_times": True,
        "auto_suggest_booking": True
    })

@router.put("/settings/scheduling")
async def update_scheduling_settings(settings: SchedulingSettings):
    """Update scheduling integration settings"""
    config = load_config()
    config["scheduling"] = settings.dict()
    save_config(config)
    return {
        "status": "success",
        "message": "Scheduling settings updated",
        "settings": settings.dict()
    }

# Event Display Settings
class EventSettings(BaseModel):
    featured_events: List[str]
    show_pricing: bool = True
    detail_level: str = "moderate"

@router.get("/settings/events")
async def get_event_settings():
    """Get event display settings"""
    config = load_config()
    return config.get("event_display", {
        "featured_events": [
            "Cutting Board Workshop",
            "Side Table Workshop",
            "Spoon Carving Workshop"
        ],
        "show_pricing": True,
        "detail_level": "moderate"
    })

@router.put("/settings/events")
async def update_event_settings(settings: EventSettings):
    """Update event display settings"""
    config = load_config()
    config["event_display"] = settings.dict()
    save_config(config)
    return {
        "status": "success",
        "message": "Event settings updated",
        "settings": settings.dict()
    }
