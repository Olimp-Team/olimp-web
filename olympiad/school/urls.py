from django.urls import path
from .views import register_school

app_name = 'school'

urlpatterns = [
    path('register/school/', register_school, name='register_school'),  # URL для регистрации школы
]
