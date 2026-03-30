from django.urls import path
from api.views import auth_views, meal_views

urlpatterns = [
    path('parse-log', meal_views.submit_food_log, name='parse_log'),
    path('register', auth_views.register, name='register'),
    path('me', auth_views.get_me, name='me'),
    path('logout', auth_views.logout, name='logout'),
]
