
# Mocking Django environment because we are outside the manage.py context
import django
from django.conf import settings

# Minimal settings for standalone run
if not settings.configured:
    settings.configure(
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
        INSTALLED_APPS=['api'],
    )
    django.setup()

from api.domain.calorie_calculator import calculate_calories

# Mock data
mock_enriched = [
    {
        "food_name": "beans",
        "quantity": 2,
        "unit": "cup",
        "calories_per_100g": 127.0,
        "grams_per_unit": 200.0,
        "default_unit": "cup"
    }
]

result = calculate_calories(mock_enriched)
print("STRUCTURE TEST:")
print(f"Top level keys: {list(result.keys())}")
if "parsed_items" in result:
    print(f"First item keys: {list(result['parsed_items'][0].keys())}")
    print(f"First item values: {result['parsed_items'][0]}")
print(f"Total calories: {result.get('total_calories')}")
