from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', AuthLogin.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),

]
