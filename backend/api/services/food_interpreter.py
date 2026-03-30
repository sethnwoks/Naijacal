import json
import logging

from api.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)


def interpret_food_log(food_log):
    logger.info("Starting food log interpretation.")

    raw_response = gemini_service.parse_food_log(food_log)

    logger.info("Gemini response received for food interpretation.")

    try:
        parsed_items = json.loads(raw_response)
    except json.JSONDecodeError:
        logger.exception("Gemini returned invalid JSON.")
        raise ValueError("AI returned invalid JSON.")

    if not isinstance(parsed_items, list):
        raise ValueError("AI response must be a list of food items.")

    validated_items = []

    for item in parsed_items:
        if not isinstance(item, dict):
            raise ValueError("Each food item must be an object.")

        food_name = item.get("food_name")
        quantity = item.get("quantity")
        unit = item.get("unit")

        if not food_name or quantity is None or not unit:
            raise ValueError(
                "Each food item must include food_name, quantity, and unit."
            )

        validated_items.append(
            {
                "food_name": str(food_name).strip().lower(),
                "quantity": quantity,
                "unit": str(unit).strip().lower(),
            }
        )

    logger.info("Food log interpretation completed successfully.")

    return validated_items