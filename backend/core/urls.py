from django.contrib import admin
from django.urls import path, include
from api.views.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView
# Make sure to import your parse_log view
# from api.views import parse_log 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth Routes
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    # App Routes
    path('', include('api.urls')),
    
    # If parse_log is not inside api.urls, keep it here:
    # path('parse-log', parse_log),
]
