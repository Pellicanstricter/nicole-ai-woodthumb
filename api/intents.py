"""
Intent classification for customer messages
"""

import json
from typing import Dict
from anthropic import Anthropic
from .config import settings
from .prompts import INTENT_CLASSIFICATION_PROMPT


class IntentClassifier:
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)

    async def classify(self, message: str) -> Dict:
        """
        Classify the intent of a customer message
        Returns: dict with intent, confidence, reasoning, and extracted entities
        """
        prompt = INTENT_CLASSIFICATION_PROMPT + message

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                temperature=0.0,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse JSON response
            response_text = response.content[0].text
            result = json.loads(response_text)

            return {
                "intent": result.get("intent", "other"),
                "confidence": result.get("confidence", 0.5),
                "reasoning": result.get("reasoning", ""),
                "entities": result.get("entities", {})
            }

        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "intent": "other",
                "confidence": 0.3,
                "reasoning": "Failed to parse intent classification",
                "entities": {}
            }
        except Exception as e:
            print(f"Intent classification error: {e}")
            return {
                "intent": "other",
                "confidence": 0.3,
                "reasoning": f"Error: {str(e)}",
                "entities": {}
            }

    def get_routing_decision(self, intent: str, confidence: float, channel: str) -> str:
        """
        Decide how to handle the response based on intent, confidence, and channel

        Returns: 'auto_send', 'draft', 'flag', or 'respond' (for chat)
        """
        # Chat always responds immediately
        if channel == "chat":
            return "respond"

        # Email routing based on confidence
        if confidence >= settings.high_confidence_threshold:
            # High confidence - auto-send for simple intents
            simple_intents = ['workshop_inquiry', 'policy_question', 'general_info']
            if intent in simple_intents:
                return "auto_send"
            else:
                return "draft"  # Even high confidence, but complex topic

        elif confidence >= settings.medium_confidence_threshold:
            # Medium confidence - save as draft
            return "draft"

        else:
            # Low confidence - flag for owner
            return "flag"


# Global classifier instance
classifier = IntentClassifier()
