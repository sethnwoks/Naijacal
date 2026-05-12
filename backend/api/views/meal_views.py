from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging

from api.services.analyze_food_log import analyze_food_log
from api.services.rate_limit_service import check_anonymous_parse_limit
import html

logger = logging.getLogger(__name__)

@api_view(["POST"])
@permission_classes([AllowAny])
def submit_food_log(request):
    """
    Public endpoint for processing natural language food logs.
    
    This view manages the end-to-end request flow:
    1. Validates the incoming payload.
    2. Enforces anonymous rate limiting (Free Trial mode).
    3. Triggers the AI-driven nutritional analysis pipeline.
    """
    raw_food_log = request.data.get("foodLog", "").strip()
    food_log = html.escape(raw_food_log)

    if not food_log:
        return JsonResponse(
            {"error": "The food log cannot be empty."},
            status=400,
        )

    if len(food_log) > 500:
        return JsonResponse(
            {"error": "Food log is too long. Please keep it under 500 characters."},
            status=400,
        )

    # Resolve identity for logging purposes (defaults to anonymous in trial mode)
    request_user = request.user.username if request.user.is_authenticated else "anonymous"
    
    # Enforce trial quotas before initiating expensive AI operations
    rate_limit_status = check_anonymous_parse_limit(request)
    if not rate_limit_status["allowed"]:
        return JsonResponse(
            {
                "error": "Daily trial limit reached. Please return in 12 hours.",
                "remaining_trials": 0,
            },
            status=429,
        )

    try:
        # Core Analysis Pipeline
        result = analyze_food_log(food_log)

        # Append trial state to the response to keep the user informed
        if rate_limit_status["remaining_trials"] is not None:
            result["remaining_trials"] = rate_limit_status["remaining_trials"]

        return JsonResponse(
            {
                "status": "success",
                **result,
            },
            status=200,
        )

    except ValueError as e:
        # Domain-level validation errors (e.g., malformed log or empty AI result)
        logger.warning(f"Analysis Failed: {str(e)} (User: {request_user})")
        return JsonResponse({"error": str(e)}, status=400)

    except Exception:
        # Catch-all for unexpected service failures
        logger.exception(f"Critical View Error: Pipeline failed for {request_user}")
        return JsonResponse(
            {"error": "An internal error occurred. Our engineers have been notified."},
            status=500,
        )
