import logging
from api.models import Food

logger = logging.getLogger(__name__)

def attach_nutrition(items: list[dict]) -> list[dict]:
    """
    Enriches a list of identified food items with nutritional benchmarks from the DB.
    
    This function performs a case-insensitive lookup for each food item. If a 
    match is not found, the item is still returned but with null nutritional 
    values, allowing the frontend to handle the 'missing data' state gracefully.
    """
    enriched = []

    for item in items:
        food_name = item.get("food_name", "").lower().strip()

        try:
            # Perform exact match (ignoring case) against our curated Nigerian food dataset
            food = Food.objects.get(name__iexact=food_name)
            enriched.append({
                **item,
                "calories_per_100g": food.calories_per_100g,
                "grams_per_unit": food.grams_per_unit,
                "default_unit": food.default_unit,
            })
        except Food.DoesNotExist:
            # Record the miss for future database enrichment but don't break the user flow
            logger.info(f"Database Miss: No nutrition data for '{food_name}'")
            enriched.append({
                **item,
                "calories_per_100g": None,
                "grams_per_unit": None,
                "default_unit": None,
            })

    return enriched