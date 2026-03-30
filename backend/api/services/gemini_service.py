import os
import logging
from itertools import cycle

from dotenv import load_dotenv
from google.genai import Client

load_dotenv()

logger = logging.getLogger(__name__)


class GeminiRotationService:
    def __init__(self):
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
            logger.critical("No Gemini API keys found in environment.")
            raise ValueError("No Gemini API keys found in environment.")

        self._keys = keys
        self._key_cycler = cycle(keys)
        self._current_key = next(self._key_cycler)

    def _rotate_key(self):
        logger.warning("Rotating Gemini API key.")
        self._current_key = next(self._key_cycler)
        logger.info("Switched to next Gemini API key.")

    def parse_food_log(self, food_log_text: str, max_retries: int = 3) -> str:
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
    "quantity": 6,
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

                logger.info(
                    "Sending food log to Gemini (attempt %s/%s).",
                    attempts + 1,
                    max_retries,
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

                if not response.text:
                    logger.error("Gemini returned an empty response body.")
                    raise ValueError("AI returned an empty response.")

                logger.info("Gemini returned a response successfully.")
                return response.text

            except Exception as e:
                error_str = str(e).lower()
                logger.error(
                    "Gemini API error on attempt %s: %s",
                    attempts + 1,
                    str(e),
                )

                if "429" in error_str or "quota" in error_str or "exhausted" in error_str:
                    attempts += 1
                    self._rotate_key()
                    continue

                raise

        logger.critical("All Gemini API keys failed after retries.")
        raise Exception("AI service unavailable. Please try again later.")


gemini_service = GeminiRotationService()
