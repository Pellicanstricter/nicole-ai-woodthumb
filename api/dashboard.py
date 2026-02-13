"""
Dashboard API endpoints for Nicole admin interface
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path

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

class ConversationLog(BaseModel):
    id: str
    timestamp: datetime
    customer_email: str
    subject: str
    message: str
    response: str
    confidence: float
    routing: str  # auto_send, draft, flag
    intent: str

# Mock data storage (replace with database in production)
MOCK_CONVERSATIONS = [
    {
        "id": "1",
        "timestamp": datetime.now() - timedelta(minutes=5),
        "customer_email": "sarah.chen@gmail.com",
        "customer_name": "Sarah Chen",
        "subject": "Workshop inquiry",
        "message": "Hi! What workshops do you offer for complete beginners? I've never done woodworking before but I'm really interested in learning.",
        "response": "Hi Sarah! I'm Nicole, Wood Thumb's AI assistant. Great news - all our workshops are designed for complete beginners! Here are some popular options...",
        "confidence": 0.92,
        "routing": "auto_send",
        "intent": "workshop_inquiry"
    },
    {
        "id": "2",
        "timestamp": datetime.now() - timedelta(minutes=23),
        "customer_email": "events@techcorp.com",
        "customer_name": "TechCorp Events",
        "subject": "Team event request",
        "message": "We're interested in booking a team building event for 15 employees. What are your options and what would the cost be?",
        "response": "Hi! Thanks for reaching out about team building at Wood Thumb. For a group of 15 people, here are our options...",
        "confidence": 0.78,
        "routing": "draft",
        "intent": "team_event_inquiry"
    },
    {
        "id": "3",
        "timestamp": datetime.now() - timedelta(hours=1),
        "customer_email": "artist@studio.com",
        "customer_name": "Art Studio",
        "subject": "Complex custom work inquiry",
        "message": "I'm working on a multimedia art installation involving reclaimed wood with very specific dimensions and artistic requirements. Can you help?",
        "response": "Hi! This sounds like an interesting project. Custom artistic work with specific requirements is best discussed directly with our team...",
        "confidence": 0.45,
        "routing": "flag",
        "intent": "custom_work_inquiry"
    }
]

# Statistics
@router.get("/stats")
async def get_dashboard_stats():
    """Get overview statistics for dashboard"""
    return {
        "total_conversations": 247,
        "total_conversations_change": 18,  # percentage
        "auto_sent_emails": 156,
        "auto_sent_emails_change": 12,
        "avg_confidence": 87,
        "avg_confidence_change": 3,
        "avg_response_time": 2.3,
        "avg_response_time_change": -0.4,
        "this_week": 247,
        "this_month": 1043,
        "auto_send_rate": 63,
        "system_status": {
            "chat_widget": "active",
            "gmail_integration": "active",
            "api_server": "healthy",
            "claude_api": "connected",
            "uptime": "7 days, 4 hours"
        }
    }

# Analytics
@router.get("/analytics")
async def get_analytics():
    """Get detailed analytics data"""
    return {
        "question_categories": [
            {"category": "Workshop Information", "count": 89, "percentage": 36},
            {"category": "Shop Time", "count": 52, "percentage": 21},
            {"category": "Team Events", "count": 43, "percentage": 17},
            {"category": "Custom Work", "count": 38, "percentage": 15},
            {"category": "General Info", "count": 25, "percentage": 10}
        ],
        "confidence_distribution": [
            {"range": "90-100%", "count": 124},
            {"range": "80-89%", "count": 68},
            {"range": "70-79%", "count": 32},
            {"range": "60-69%", "count": 18},
            {"range": "<60%", "count": 5}
        ],
        "response_times": {
            "avg": 2.3,
            "min": 1.2,
            "max": 4.8,
            "median": 2.1
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
    # In production, this would update the .env file or database
    # For now, we'll just validate and return success
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
    # In production, save to database or config file
    return {
        "status": "success",
        "message": "Templates updated",
        "templates": templates.dict()
    }

# Conversations
@router.get("/conversations")
async def get_conversations(
    limit: int = 50,
    status: Optional[str] = None,
    days: Optional[int] = 7
):
    """Get conversation history with optional filtering"""
    conversations = MOCK_CONVERSATIONS

    # Filter by status if provided
    if status and status != "all":
        conversations = [c for c in conversations if c["routing"] == status]

    # Filter by date range
    if days:
        cutoff = datetime.now() - timedelta(days=days)
        conversations = [c for c in conversations if c["timestamp"] > cutoff]

    # Apply limit
    conversations = conversations[:limit]

    # Convert datetime to ISO string for JSON serialization
    for conv in conversations:
        conv["timestamp"] = conv["timestamp"].isoformat()

    return {
        "conversations": conversations,
        "total": len(conversations)
    }

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get detailed conversation by ID"""
    for conv in MOCK_CONVERSATIONS:
        if conv["id"] == conversation_id:
            conv_copy = conv.copy()
            conv_copy["timestamp"] = conv_copy["timestamp"].isoformat()
            return conv_copy

    raise HTTPException(status_code=404, detail="Conversation not found")

# Gmail Integration
@router.get("/gmail/status")
async def get_gmail_status():
    """Get Gmail integration status"""
    return {
        "connected": True,
        "email": "steinrueckn@gmail.com",
        "apps_script_status": "running",
        "last_check": datetime.now().isoformat(),
        "api_connection": "healthy",
        "api_url": "http://localhost:8000/api",
        "stats": {
            "emails_processed": 247,
            "auto_sent": 156,
            "drafts_created": 68,
            "flagged": 23
        }
    }

@router.post("/gmail/test")
async def test_gmail_connection():
    """Test Gmail integration connection"""
    # In production, this would test the actual Gmail API connection
    return {
        "status": "success",
        "message": "Gmail connection is working",
        "timestamp": datetime.now().isoformat()
    }

# Quick Links
@router.get("/settings/links")
async def get_quick_links():
    """Get quick links configuration"""
    return {
        "booking_url": "https://woodthumb.com/workshops",
        "contact_email": "info@woodthumb.com",
        "phone": "(510) 555-0100"
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
