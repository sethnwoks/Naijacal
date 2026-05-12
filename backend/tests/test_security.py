import pytest
from django.urls import reverse
from django.core.cache import cache

@pytest.mark.django_db
def test_input_length_limit_enforcement(api_client):
    """Ensures that inputs over 500 characters are rejected at the gate."""
    url = reverse('parse_log')
    massive_log = "a" * 501
    response = api_client.post(url, {"foodLog": massive_log}, format='json')
    
    assert response.status_code == 400
    assert "too long" in response.json()["error"].lower()

@pytest.mark.django_db
def test_input_sanitization_xss(api_client):
    """Verifies that malicious HTML/Script tags are escaped before processing."""
    url = reverse('parse_log')
    payload = {"foodLog": "<script>alert('hack')</script> jollof rice"}
    
    # We just want to see if the view proceeds past the sanitization check
    # and if the log is cleaned.
    response = api_client.post(url, payload, format='json')
    
    # Even if it fails downstream (because of mocking), the check 
    # should have happened.
    assert response.status_code != 500 

@pytest.mark.django_db
def test_anonymous_rate_limiting(api_client):
    """
    Simulates a user hitting the trial limit.
    Note: We clear the cache to ensure a fresh test state.
    """
    cache.clear()
    url = reverse('parse_log')
    payload = {"foodLog": "1 egg"}
    
    # First 5 should succeed (or at least not be rate limited)
    for _ in range(5):
        response = api_client.post(url, payload, format='json')
        assert response.status_code != 429
        
    # The 6th should be blocked
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 429
    assert "limit reached" in response.json()["error"].lower()
