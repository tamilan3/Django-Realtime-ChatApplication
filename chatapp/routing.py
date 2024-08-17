from django.urls import re_path
from .consumers import chat_consumers,vidio_consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', chat_consumers.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/videocall/(?P<room_name>\w+)/$', vidio_consumers.VideoCallConsumer.as_asgi()),
]