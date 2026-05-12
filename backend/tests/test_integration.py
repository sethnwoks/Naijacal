import pytest
import json
from unittest.mock import patch
from django.urls import reverse

@pytest.mark.django_db
def test_parse_log_integration_success(api_client, seed_nutrition_data):
    """
    Tests the full request cycle: View -> Mock AI -> DB Enrichment -> Calculation.
    """
    url = reverse('parse_log')
    payload = {"foodLog": "I had 2 plates of jollof rice"}
    
    # Mock the LLM service to return a fixed JSON structure
    mock_ai_response = json.dumps([
        {"food_name": "jollof rice", "quantity": 2, "unit": "plate"}
    ])
    
    with patch('api.services.gemini_service.gemini_service.parse_food_log', return_value=mock_ai_response):
        response = api_client.post(url, payload, format='json')
        
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total_calories"] == 2000.0 # (250/100) * 400 * 2
    assert len(data["parsed_items"]) == 1
    assert data["parsed_items"][0]["item"] == "jollof rice"

@pytest.mark.django_db
def test_parse_log_malformed_ai_response(api_client):
    """Verifies that the system handles invalid JSON from the AI gracefully."""
    url = reverse('parse_log')
    payload = {"foodLog": "Something weird"}
    
    with patch('api.services.gemini_service.gemini_service.parse_food_log', return_value="Invalid JSON"):
        response = api_client.post(url, payload, format='json')
        
    assert response.status_code == 400
    assert "error" in response.json()

@pytest.mark.django_db
def test_parse_log_empty_input(api_client):
    """Ensures that the API rejects empty logs before hitting the AI."""
    url = reverse('parse_log')
    response = api_client.post(url, {"foodLog": ""}, format='json')
    
    assert response.status_code == 400
    assert "error" in response.json()
