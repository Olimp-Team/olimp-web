from django.urls import path
from .views import login_view
app_name = 'api'


urlpatterns = [
    path('api/login/', login_view, name='api-login'),
]
