from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('password_change/', password_change, name='password_change'),

]
