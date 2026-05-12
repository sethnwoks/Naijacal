"""
Domain logic for nutritional calculations.

This module provides a deterministic engine to calculate caloric totals 
based on a 100g benchmark. It handles the mapping of various measurement 
units (cups, wraps, etc.) to a standard gram-weight to ensure consistency 
across the Nigerian food dataset.
"""

# Standard conversion table for common Nigerian food measurements.
# Values represent the estimated weight in grams for one unit of the item.
UNIT_TO_GRAMS = {
    "g": 1,
    "gram": 1,
    "grams": 1,
    "kg": 1000,
    "kilogram": 1000,
    "kilograms": 1000,
    "cup": 200,
    "cups": 200,
    "derica": 250,
    "wrap": 250,
    "wraps": 250,
    "bowl": 300,
    "bowls": 300,
    "plate": 400,
    "plates": 400,
    "handful": 28,
    "handfuls": 28,
    "tablespoon": 15,
    "tablespoons": 15,
    "slice": 60,
    "slices": 60,
    "piece": 100,
    "pieces": 100,
}

def calculate_calories(enriched_items: list[dict]) -> dict:
    """
    Orchestrates the calculation pipeline for a list of food items.
    
    Expects items already enriched with database-level nutrition data 
    (calories_per_100g and grams_per_unit).
    """
    results = []
    total_kcal = 0.0

    for item in enriched_items:
        cal_per_100g = item.get("calories_per_100g")
        grams_per_unit = item.get("grams_per_unit")
        default_unit = item.get("default_unit")
        quantity = item.get("quantity", 0)
        unit = item.get("unit", "").lower().strip()

        # Gracefully handle items missing from the local nutrition database
        if not cal_per_100g or not grams_per_unit:
            results.append({
                "item": item["food_name"], 
                "total_calories": None, 
                "note": "Item not found in local database"
            })
            continue

        # Convert the item's current unit to a total gram weight for standardizing
        if unit == default_unit:
            total_grams = quantity * grams_per_unit
        else:
            total_grams = quantity * UNIT_TO_GRAMS.get(unit, grams_per_unit)

        # Standard calculation: (kcal / 100g) * total_weight_in_g
        item_calories = (cal_per_100g / 100) * total_grams

        results.append({
            "item": item["food_name"],
            "quantity": quantity,
            "unit": unit,
            "total_calories": round(item_calories, 1)
        })
        total_kcal += item_calories

    return {
        "parsed_items": results,
        "total_calories": round(total_kcal, 1)
    }
