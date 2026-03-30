import logging

from api.services.food_interpreter import interpret_food_log
from api.repositories.food_repository import attach_nutrition
from api.domain.calorie_calculator import calculate_calories

logger = logging.getLogger(__name__)


def analyze_food_log(food_log):
    logger.info("Starting food log analysis workflow.")

    items = interpret_food_log(food_log)
    nutrition_items = attach_nutrition(items)
    result = calculate_calories(nutrition_items)

    logger.info("Food log analysis workflow completed successfully.")

    return result
