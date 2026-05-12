import json
import logging
from api.services.gemini_service import gemini_service

logger = logging.getLogger(__name__)

def interpret_food_log(food_log: str) -> list[dict]:
    """
    Coordinates the translation of raw text logs into validated food objects.
    
    This function acts as a bridge between the LLM's raw response and the 
    application's internal data structures, ensuring that only correctly 
    formatted data enters the calculation pipeline.
    """
    raw_response = gemini_service.parse_food_log(food_log)

    try:
        parsed_items = json.loads(raw_response)
    except json.JSONDecodeError:
        logger.exception("AI Response Error: Returned data was not valid JSON.")
        raise ValueError("The AI service returned a malformed response.")

    if not isinstance(parsed_items, list):
        raise ValueError("Invalid Data Structure: Expected a list of items.")

    validated_items = []

    # Clean and validate each entry to prevent downstream calculation errors
    for item in parsed_items:
        if not isinstance(item, dict):
            continue

        food_name = item.get("food_name")
        quantity = item.get("quantity")
        unit = item.get("unit")

        if not all([food_name, quantity is not None, unit]):
            logger.warning(f"Validation Warning: Skipping incomplete item: {item}")
            continue

        validated_items.append({
            "food_name": str(food_name).strip().lower(),
            "quantity": quantity,
            "unit": str(unit).strip().lower(),
        })

    if not validated_items:
        raise ValueError("No valid food items could be identified in the log.")

    return validated_items