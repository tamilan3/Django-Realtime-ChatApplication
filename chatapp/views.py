"""Chat application views module.

This module contains views for handling chat rooms and video calls.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .models import ChatMessage


class IndexView(LoginRequiredMixin, TemplateView):
    """Main chat index view."""

    template_name = "chatapp/index.html"
    login_url = "/auth/login/"


class ChatRoomView(LoginRequiredMixin, View):
    """View for handling chat room functionality.

    This view manages the chat room interface, displaying messages and handling
    user interactions within a specific chat room.
    """

    template_name = "chatapp/room.html"
    login_url = "/auth/login/"

    def get(self, request, room_name):
        """Handle GET requests for the chat room.

        Args:
            request: The HTTP request object
            room_name: The name of the chat room to display

        Returns:
            Rendered template with chat room context
        """
        username = request.user.username
        messages = ChatMessage.objects.filter(room=room_name).order_by("timestamp")
        context = {
            "room_name": room_name,
            "username": username,
            "messages": messages,
        }
        return render(request, self.template_name, context)


class VideoChatView(LoginRequiredMixin, View):
    """View for handling video chat functionality."""

    template_name = "chatapp/videocall.html"
    login_url = "/auth/login/"

    def get(self, request, room_name):
        """Handle GET requests for the video chat room.

        Args:
            request: The HTTP request object
            room_name: The name of the video chat room

        Returns:
            Rendered template with video chat context
        """
        username = request.user.username
        messages = ChatMessage.objects.filter(room=room_name)
        users = ChatMessage.objects.filter(room=room_name).values("user").distinct()
        context = {
            "room_name": room_name,
            "username": username,
            "messages": messages,
            "users": users,
        }
        return render(request, self.template_name, context)
