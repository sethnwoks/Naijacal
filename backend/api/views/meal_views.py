from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import logging

from api.services.analyze_food_log import analyze_food_log
from api.services.rate_limit_service import check_anonymous_parse_limit

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([AllowAny])
def submit_food_log(request):
    food_log = request.data.get("foodLog", "").strip()

    if not food_log:
        return JsonResponse(
            {"error": "foodLog is required and must be a non-empty string."},
            status=400,
        )

    username = request.user.username if request.user.is_authenticated else "anonymous"
    rate_limit_status = check_anonymous_parse_limit(request)

    if not rate_limit_status["allowed"]:
        return JsonResponse(
            {
                "error": "Free trial limit reached. Please try again in 12 hours.",
                "remaining_trials": 0,
            },
            status=429,
        )

    try:
        logger.info("Food log received from user: %s", username)

        result = analyze_food_log(food_log)

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
        logger.warning(
            "Food log validation error for user %s: %s",
            username,
            str(e),
        )
        return JsonResponse({"error": str(e)}, status=400)

    except Exception:
        logger.exception(
            "Unexpected error while processing food log for user: %s",
            username,
        )
        return JsonResponse(
            {"error": "An unexpected error occurred while processing the food log."},
            status=500,
        )
