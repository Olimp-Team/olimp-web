from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
app_name = 'api'

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-password/', RequestPasswordResetView.as_view(), name='request_reset_password'),
    path('reset-password/<uid>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
]
