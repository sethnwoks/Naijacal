import logging
from api.services.food_interpreter import interpret_food_log
from api.repositories.food_repository import attach_nutrition
from api.domain.calorie_calculator import calculate_calories

logger = logging.getLogger(__name__)

def analyze_food_log(food_log: str) -> dict:
    """
    Orchestrates the multi-stage pipeline to transform text into calorie data.
    
    The workflow follows a 3-step sequence:
    1. AI Interpretation: Extract items, quantities, and units from text.
    2. Data Enrichment: Fetch nutritional benchmarks from the local database.
    3. Calculation: Compute final caloric totals based on standardized weights.
    """
    
    # Stage 1: LLM Extraction
    items = interpret_food_log(food_log)
    
    # Stage 2: Database Matching
    nutrition_items = attach_nutrition(items)
    
    # Stage 3: Domain Math
    return calculate_calories(nutrition_items)
