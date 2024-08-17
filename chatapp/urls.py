from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.chat_room, name='room'),
    # path('chat/<str:room_name>/detail/', views.chat_detail, name='chat_detail'),
    path("video-chat/<str:room_name>/", views.video_chat, name="video_call"),
]