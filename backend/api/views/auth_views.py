import logging
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.response import Response

logger = logging.getLogger(__name__)
AUTH_DISABLED_MESSAGE = "Authentication is temporarily unavailable."


def auth_disabled_response():
    return JsonResponse({"error": AUTH_DISABLED_MESSAGE}, status=503)


def set_jwt_cookie(response, refresh_token):
    # Determine secure flag based on DEBUG. If deploying to production (DEBUG=False), secure is True.
    is_secure = not settings.DEBUG
    # Setting the generic refresh_token cookie
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=is_secure,
        samesite='Lax',
        max_age=7 * 24 * 60 * 60 # 7 days
    )
    return response

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        if not settings.AUTH_ENABLED:
            return Response({"error": AUTH_DISABLED_MESSAGE}, status=503)

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            if refresh_token:
                response = set_jwt_cookie(response, refresh_token)
                del response.data['refresh'] # Don't send it in body
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        if not settings.AUTH_ENABLED:
            return Response({"error": AUTH_DISABLED_MESSAGE}, status=503)

        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            # Inject it into request data mimicking what the serializer expects
            # Django REST request.data is sometimes immutable (QueryDict), so we use a mutable copy if needed
            if hasattr(request.data, '_mutable'):
                request.data._mutable = True
            request.data['refresh'] = refresh_token
        
        try:
            response = super().post(request, *args, **kwargs)
        except InvalidToken:
            return Response({"error": "Invalid or expired refresh token"}, status=401)
        
        if response.status_code == 200 and 'refresh' in response.data:
            new_refresh = response.data.get('refresh')
            response = set_jwt_cookie(response, new_refresh)
            del response.data['refresh']
            
        return response

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if not settings.AUTH_ENABLED:
        return auth_disabled_response()

    data = request.data
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)

    try:
        user = User.objects.create_user(username=username, password=password)
        logger.info(f"User created securely: {username}")
    except IntegrityError:
        logger.warning(f"Registration failed - username already exists: {username}")
        return JsonResponse({"error": "Username already exists."}, status=409)
    except Exception as e:
        logger.error(f"Registration failed due to unexpected error: {str(e)}")
        return JsonResponse({"error": "Could not register user"}, status=500)

    refresh = RefreshToken.for_user(user)

    response = JsonResponse({
        "username": user.username,
        "access": str(refresh.access_token)
    })
    
    return set_jwt_cookie(response, str(refresh))

@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    if not settings.AUTH_ENABLED:
        return auth_disabled_response()

    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("Successfully blacklisted refresh token on logout.")
        except Exception as e:
            logger.warning(f"Failed to blacklist token or token already invalid: {str(e)}")

    response = JsonResponse({"status": "success", "message": "Successfully logged out"})
    response.delete_cookie('refresh_token')
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    if not settings.AUTH_ENABLED:
        return auth_disabled_response()

    # Returns the currently logged in user's info
    return JsonResponse({
        "username": request.user.username,
        "email": request.user.email
    })
