"""
Simple JSON-based conversation storage for Nicole
Logs all chat widget conversations for dashboard review
Uses /data volume on Railway for persistence across deploys
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# Use /data on Railway (persistent volume), local path otherwise
if os.path.isdir('/data'):
    CONVERSATIONS_FILE = Path('/data/conversations.json')
else:
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


RETENTION_DAYS = 90


def _purge_old(conversations: List[dict]) -> List[dict]:
    """Remove conversations older than RETENTION_DAYS"""
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(days=RETENTION_DAYS)).isoformat()
    return [c for c in conversations if c.get("timestamp", "") >= cutoff]


def log_conversation(session_id: Optional[str], user_message: str, nicole_response: str):
    """Log a single conversation exchange"""
    conversations = _load_conversations()

    # Purge old conversations on every write
    conversations = _purge_old(conversations)

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

    return conversations[:limit]


def get_session_conversations(session_id: str) -> List[dict]:
    """Get all messages in a specific session"""
    conversations = _load_conversations()
    return [c for c in conversations if c.get("session_id") == session_id]
