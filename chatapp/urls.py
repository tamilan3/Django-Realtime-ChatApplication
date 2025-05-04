"""Chat application URL configuration.

This module defines the URL patterns for chat room and video call views.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("chat/<str:room_name>/", views.ChatRoomView.as_view(), name="room"),
    path(
        "video-chat/<str:room_name>/", views.VideoChatView.as_view(), name="video_call"
    ),
]
