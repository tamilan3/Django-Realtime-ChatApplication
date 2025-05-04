"""Chat application WebSocket routing configuration.

This module defines the WebSocket URL patterns for chat and video call functionality.
"""

from django.urls import re_path

from .consumers import chat_consumers, video_consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", chat_consumers.ChatRoomConsumer.as_asgi()),
    re_path(
        r"ws/videocall/(?P<room_name>\w+)/$",
        video_consumers.VideoCallConsumer.as_asgi(),
    ),
]
