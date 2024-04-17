from rest_framework import routers
from .views import *
from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('users-list/', ChildrenApiReact.as_view(), name='users-list'),


]
