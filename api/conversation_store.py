"""
Simple JSON-based conversation storage for Nicole
Logs all chat widget conversations for dashboard review
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

CONVERSATIONS_FILE = Path(__file__).parent / "conversations.json"


def _load_conversations() -> List[dict]:
    """Load all conversations from file"""
    if CONVERSATIONS_FILE.exists():
        try:
            with open(CONVERSATIONS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_conversations(conversations: List[dict]):
    """Save conversations to file"""
    with open(CONVERSATIONS_FILE, 'w') as f:
        json.dump(conversations, f, indent=2, default=str)


def log_conversation(session_id: Optional[str], user_message: str, nicole_response: str):
    """Log a single conversation exchange"""
    conversations = _load_conversations()

    entry = {
        "id": str(uuid.uuid4())[:8],
        "session_id": session_id or str(uuid.uuid4())[:8],
        "timestamp": datetime.now().isoformat(),
        "user_message": user_message,
        "nicole_response": nicole_response,
    }

    conversations.append(entry)
    _save_conversations(conversations)


def get_conversations(limit: int = 50, days: Optional[int] = None) -> List[dict]:
    """Get conversations with optional filtering"""
    conversations = _load_conversations()

    # Filter by date range
    if days:
        from datetime import timedelta
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        conversations = [c for c in conversations if c.get("timestamp", "") >= cutoff]

    # Sort newest first
    conversations.sort(key=lambda c: c.get("timestamp", ""), reverse=True)

    # Group by session_id for display
    return conversations[:limit]


def get_session_conversations(session_id: str) -> List[dict]:
    """Get all messages in a specific session"""
    conversations = _load_conversations()
    return [c for c in conversations if c.get("session_id") == session_id]
