import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Food

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="password123")

@pytest.fixture
def seed_nutrition_data(db):
    """Populates the test database with standard Nigerian food items."""
    Food.objects.create(name="jollof rice", calories_per_100g=250, grams_per_unit=400, default_unit="plate")
    Food.objects.create(name="boiled egg", calories_per_100g=155, grams_per_unit=50, default_unit="piece")
    Food.objects.create(name="pounded yam", calories_per_100g=120, grams_per_unit=250, default_unit="wrap")
