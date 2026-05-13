import os
import logging
from itertools import cycle
from dotenv import load_dotenv
from google.genai import Client

load_dotenv()
logger = logging.getLogger(__name__)

class LLMRotationService:
    """
    Orchestrates LLM requests with high availability via API key rotation.
    
    This service ensures that the application remains functional even when 
    individual API keys hit quota limits (429 errors). It cycles through 
    a pool of available keys to maximize uptime for the free trial tier.
    """
    def __init__(self):
        # Initialize the pool from environment variables (up to 3 keys)
        keys = [
            key
            for key in (
                os.getenv("GEMINI_API_KEY_1"),
                os.getenv("GEMINI_API_KEY_2"),
                os.getenv("GEMINI_API_KEY_3"),
            )
            if key
        ]

        if not keys:
            logger.critical("AI configuration error: No provider keys found.")
            raise ValueError("No LLM API keys found in environment.")

        self._keys = keys
        self._key_cycler = cycle(keys)
        self._current_key = next(self._key_cycler)

    def _rotate_key(self):
        """Switches the active API key in the pool."""
        self._current_key = next(self._key_cycler)
        logger.info("Service: Rotated to next available AI provider key.")

    def parse_food_log(self, food_log_text: str, max_retries: int = 3) -> str:
        """
        Interprets natural language food logs into structured JSON.
        
        Uses a strictly-formatted prompt to ensure the LLM returns a parseable 
        JSON array without conversational filler or markdown fences.
        """
        prompt = f"""
You are a Nigerian nutrition expert AI.

TASK:
Parse the user's food log into valid JSON only.

Return ONLY a JSON array.
Do not add markdown.
Do not add explanations.
Do not wrap in code fences.

Each item must follow this structure:
[
  {{
    "food_name": "egg",
    "quantity": 1,
    "unit": "piece"
  }}
]

FOOD LOG:
{food_log_text}
""".strip()

        attempts = 0
        while attempts < max_retries:
            try:
                client = Client(api_key=self._current_key)
                
                # Request inference from a high-speed Flash model
                model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )

                if not response.text:
                    raise ValueError("LLM returned an empty response body.")

                return response.text

            except Exception as e:
                error_msg = str(e).lower()
                logger.error(f"AI Service: Attempt {attempts + 1} failed with error: {error_msg}")

                # Automatic failover: try the next key for ANY error
                attempts += 1
                if attempts < max_retries:
                    logger.warning(f"AI Service: Rotating key and retrying... (Attempt {attempts + 1})")
                    self._rotate_key()
                    continue

                # If all retries fail, raise the final error
                logger.critical("AI Service: All failover attempts exhausted.")
                raise

        logger.critical("Critical Failure: All AI provider keys in the pool are exhausted.")
        raise Exception("AI service temporarily unavailable due to high demand.")

# Global singleton instance for app-wide use
gemini_service = LLMRotationService()
