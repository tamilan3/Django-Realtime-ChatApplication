"""Chat application URL configuration.

This module defines the URL patterns for chat room and video call views.
"""

from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'chat'  # Add URL namespace

urlpatterns = [
    path("", login_required(views.IndexView.as_view()), name="index"),
    path("<str:room_name>/", login_required(views.ChatRoomView.as_view()), name="room"),
    path(
        "video-chat/<str:room_name>/", 
        login_required(views.VideoChatView.as_view()), 
        name="video_call"
    ),
]
