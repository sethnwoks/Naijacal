import pytest
from api.domain.calorie_calculator import calculate_calories

@pytest.mark.parametrize("food_items, expected_total", [
    # Happy Path: Standard units
    ([
        {"food_name": "jollof rice", "quantity": 1, "unit": "plate", "calories_per_100g": 250, "grams_per_unit": 400, "default_unit": "plate"}
    ], 1000.0), # (250/100) * 400 * 1 = 1000
    
    # Happy Path: Unit conversion (2 wraps of 250g each)
    ([
        {"food_name": "pounded yam", "quantity": 2, "unit": "wrap", "calories_per_100g": 120, "grams_per_unit": 250, "default_unit": "wrap"}
    ], 600.0), # (120/100) * 250 * 2 = 600
    
    # Edge Case: Unknown unit (should fallback to grams_per_unit)
    ([
        {"food_name": "unknown food", "quantity": 1, "unit": "random", "calories_per_100g": 100, "grams_per_unit": 100, "default_unit": "piece"}
    ], 100.0),
    
    # Edge Case: Missing data (should return None for that item and continue)
    ([
        {"food_name": "missing food", "quantity": 1, "unit": "plate", "calories_per_100g": None, "grams_per_unit": None}
    ], 0.0),
])
def test_calorie_calculation_logic(food_items, expected_total):
    """Verifies that the math engine correctly standardizes units and calculates kcal."""
    result = calculate_calories(food_items)
    assert result["total_calories"] == expected_total

def test_calorie_calculation_rounding():
    """Ensures that the output is rounded to 1 decimal place as per requirements."""
    item = [{"food_name": "precise food", "quantity": 1, "unit": "g", "calories_per_100g": 123.456, "grams_per_unit": 1, "default_unit": "g"}]
    result = calculate_calories(item)
    assert result["total_calories"] == 1.2 # (123.456/100) * 1 = 1.23456 -> 1.2
