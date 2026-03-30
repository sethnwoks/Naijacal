from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import json
import logging
from .utils import parse_food_log

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny]) # Anyone can sign up
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')

        if not username or not password:
            return JsonResponse({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        
        # Log them in automatically by returning tokens
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            "message": "User created successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    # Returns the currently logged in user's info
    return JsonResponse({
        "username": request.user.username,
        "email": request.user.email
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Only logged in users can parse
def parse_log(request):
    try:
        data = json.loads(request.body)
        if not data or 'foodLog' not in data:
            return JsonResponse({"error": "Invalid request. 'foodLog' key is missing."}, status=400)

        food_log = data['foodLog']
        parsed_items, total_calories = parse_food_log(food_log)

        return JsonResponse({
            "status": "success",
            "parsed_items": parsed_items,
            "total_calories": total_calories
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
