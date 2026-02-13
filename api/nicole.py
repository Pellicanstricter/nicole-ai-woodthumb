"""
Nicole Core AI Logic
Handles conversations using Claude API
"""

from typing import List, Dict, Optional, AsyncIterator
from anthropic import Anthropic, AsyncAnthropic
from .config import settings
from .prompts import get_system_prompt
from .intents import classifier


class Nicole:
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.async_client = AsyncAnthropic(api_key=settings.anthropic_api_key)

    def generate_response(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        stream: bool = False
    ):
        """
        Generate a response to a customer message

        Args:
            message: The customer's message
            conversation_history: List of previous messages [{"role": "user"|"assistant", "content": "..."}]
            stream: Whether to stream the response

        Returns:
            Dict with response text, intent, confidence, and routing decision (if not streaming)
            OR AsyncGenerator yielding chunks (if streaming)
        """

        if stream:
            # Return async generator for streaming
            return self._generate_response_stream(message, conversation_history)
        else:
            # Return coroutine for non-streaming
            return self._generate_response_sync(message, conversation_history)

    async def _generate_response_sync(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict:
        """Non-streaming response generation"""
        # Build message history
        messages = conversation_history if conversation_history else []
        messages.append({"role": "user", "content": message})

        try:
            # Get fresh system prompt with current dashboard settings
            system_prompt = get_system_prompt()

            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=800,  # Sufficient for detailed responses with lists
                system=system_prompt,
                messages=messages
            )

            response_text = response.content[0].text

            return {
                "response": response_text
            }

        except Exception as e:
            error_msg = "I'm having trouble connecting right now. Email nicole@woodthumb.com or call (415) 295-5047."
            print(f"Nicole error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "response": error_msg,
                "intent": "other",
                "confidence": 0.0,
                "reasoning": "Error occurred",
                "entities": {},
                "error": str(e)
            }

    async def _generate_response_stream(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ):
        """Streaming response generation"""
        # Build message history
        messages = conversation_history if conversation_history else []
        messages.append({"role": "user", "content": message})

        try:
            # Get fresh system prompt with current dashboard settings
            system_prompt = get_system_prompt()

            response_text = ""
            async with self.async_client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=800,  # Sufficient for detailed responses with lists
                system=system_prompt,
                messages=messages
            ) as stream:
                async for text in stream.text_stream:
                    response_text += text
                    yield {
                        "type": "chunk",
                        "content": text
                    }

            # Final result
            yield {
                "type": "complete",
                "response": response_text
            }

        except Exception as e:
            error_msg = "I'm having trouble connecting right now. Email nicole@woodthumb.com or call (415) 295-5047."
            print(f"Nicole error: {e}")
            import traceback
            traceback.print_exc()
            yield {
                "type": "error",
                "error": error_msg
            }

    async def generate_email_response(
        self,
        subject: str,
        body: str,
        from_email: str
    ) -> Dict:
        """
        Generate a response specifically for email

        Returns:
            Dict with response, intent, confidence, and routing decision
        """

        # Combine subject and body for analysis
        full_message = f"Subject: {subject}\n\n{body}"

        # Classify intent
        intent_result = await classifier.classify(full_message)

        # Get routing decision
        routing = classifier.get_routing_decision(
            intent_result["intent"],
            intent_result["confidence"],
            channel="email"
        )

        # Generate response
        messages = [{
            "role": "user",
            "content": f"Customer email from {from_email}\n\nSubject: {subject}\n\n{body}"
        }]

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=SYSTEM_PROMPT + "\n\nIMPORTANT: You are responding to an email. Format your response as a complete email reply with appropriate greeting and signature.",
                messages=messages
            )

            response_text = response.content[0].text

            return {
                "response": response_text,
                "intent": intent_result["intent"],
                "confidence": intent_result["confidence"],
                "reasoning": intent_result["reasoning"],
                "entities": intent_result["entities"],
                "routing": routing,
                "from_email": from_email,
                "original_subject": subject,
                "original_body": body
            }

        except Exception as e:
            print(f"Email response error: {e}")
            return {
                "response": "Error generating response",
                "intent": "other",
                "confidence": 0.0,
                "reasoning": "Error occurred",
                "entities": {},
                "routing": "flag",
                "error": str(e)
            }


# Global Nicole instance
nicole = Nicole()
