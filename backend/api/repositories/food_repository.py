import logging

from api.models import Food

logger = logging.getLogger(__name__)


def attach_nutrition(items: list[dict]) -> list[dict]:
    enriched = []

    for item in items:
        food_name = item.get("food_name", "").lower().strip()

        try:
            food = Food.objects.get(name__iexact=food_name)
            logger.debug("Matched food: '%s'", food_name)
            enriched.append({
                **item,
                "calories_per_100g": food.calories_per_100g,
                "grams_per_unit": food.grams_per_unit,
                "default_unit": food.default_unit,
            })
        except Food.DoesNotExist:
            logger.warning("Food not found in DB: '%s'", food_name)
            enriched.append({
                **item,
                "calories_per_100g": None,
                "grams_per_unit": None,
                "default_unit": None,
            })

    return enriched