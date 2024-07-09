from django.urls import path
from .views import *

app_name = 'friends'

urlpatterns = [
    path('add_friend/<int:user_id>/', add_friend, name='add_friend'),
    path('accept_friend_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
    path('', view_friends, name='view_friends'),
    path('friend_requests/', view_friend_requests, name='view_friend_requests'),
    path('search_friends/', search_friends, name='search_friends'),
    path('save_cropped_image/', save_cropped_image, name='save_cropped_image'),
]
