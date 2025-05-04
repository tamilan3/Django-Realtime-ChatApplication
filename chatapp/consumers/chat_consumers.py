"""Chat WebSocket consumers module.

This module contains the WebSocket consumer for handling real-time chat functionality,
including message handling, user status tracking, and typing indicators.
"""

import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from ..models import ChatMessage, ChatRoom


class ChatRoomConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for chat room functionality."""

    connected_users = {}  # Class variable to track connected users per room

    async def connect(self):
        """Handle new WebSocket connection."""
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]

        if self.room_name not in self.connected_users:
            self.connected_users[self.room_name] = set()
        self.connected_users[self.room_name].add(self.user.username)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_list_update",
                "users": list(self.connected_users[self.room_name]),
            },
        )

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if hasattr(self, "user") and hasattr(self, "room_name"):
            if self.room_name in self.connected_users:
                self.connected_users[self.room_name].discard(self.user.username)
                if not self.connected_users[self.room_name]:
                    del self.connected_users[self.room_name]

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_list_update",
                    "users": list(self.connected_users.get(self.room_name, [])),
                },
            )

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username")
        typing_status = text_data_json.get("typing")
        room_name = self.room_name

        if message:
            try:
                user = await sync_to_async(User.objects.get)(username=username)
                room, created = await sync_to_async(ChatRoom.objects.get_or_create)(
                    name=room_name
                )
                chat_message = ChatMessage(user=user, room=room, message=message)
                await sync_to_async(chat_message.save)()

            except Exception as e:
                print(e)
            finally:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "chat_message", "message": message, "username": username},
                )
        elif typing_status == "typing":
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "user_typing", "username": username}
            )

    async def chat_message(self, event):
        """Send chat message to WebSocket."""
        message = event["message"]
        username = event["username"]

        await self.send(
            text_data=json.dumps({"message": message, "username": username})
        )

    async def user_typing(self, event):
        """Send typing indicator to WebSocket."""
        username = event["username"]

        await self.send(text_data=json.dumps({"typing": True, "username": username}))

    async def user_list_update(self, event):
        """Send updated user list to WebSocket."""
        await self.send(
            text_data=json.dumps({"type": "user_list_update", "users": event["users"]})
        )
