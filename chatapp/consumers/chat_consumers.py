"""Chat WebSocket consumers module.

This module contains the WebSocket consumer for handling real-time chat functionality,
including message handling, user status tracking, and typing indicators.
"""

import json
from collections import defaultdict

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from ..models import ChatMessage, ChatRoom

User = get_user_model()

class ChatRoomConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for chat room functionality."""

    connected_users = {}  # Class variable to track connected users per room
    room_connections = defaultdict(int)  # Track number of connections per room
    MAX_ROOM_CONNECTIONS = 5  # Maximum connections per room

    async def connect(self):
        """Handle new WebSocket connection."""
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        try:
            # Check room connection limit
            if self.room_connections[self.room_name] >= self.MAX_ROOM_CONNECTIONS:
                await self.close(code=4001)  # Custom close code for room full
                return

            # Initialize room users if needed
            if self.room_name not in self.connected_users:
                self.connected_users[self.room_name] = set()
            
            # Add user and increment connection count
            self.connected_users[self.room_name].add(self.user.username)
            self.room_connections[self.room_name] += 1

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

            # Send initial room state
            await self.send_room_state()
            
        except Exception as e:
            print(f"Error in connect: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        try:
            if hasattr(self, "user") and hasattr(self, "room_name"):
                if self.room_name in self.connected_users:
                    self.connected_users[self.room_name].discard(self.user.username)
                    self.room_connections[self.room_name] -= 1
                    
                    if self.room_connections[self.room_name] <= 0:
                        del self.connected_users[self.room_name]
                        del self.room_connections[self.room_name]
                    
                    await self.send_room_state()

            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        except Exception as e:
            print(f"Error in disconnect: {str(e)}")

    async def send_room_state(self):
        """Send current room state to all connected users."""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "room_state_update",
                "users": list(self.connected_users.get(self.room_name, [])),
                "connection_count": self.room_connections.get(self.room_name, 0),
                "max_connections": self.MAX_ROOM_CONNECTIONS
            },
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message = data.get("message")
            username = data.get("username")
            typing_status = data.get("typing")
            
            if message and username:
                # Store message in database
                try:
                    user = await sync_to_async(User.objects.get)(username=username)
                    room, created = await sync_to_async(ChatRoom.objects.get_or_create)(
                        name=self.room_name
                    )
                    chat_message = await sync_to_async(ChatMessage.objects.create)(
                        user=user,
                        room=room,
                        message=message
                    )
                    
                    # Format timestamp
                    timestamp = await sync_to_async(lambda: chat_message.timestamp.strftime("%I:%M %p"))()
                    
                    # Broadcast message
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "chat_message",
                            "message": message,
                            "username": username,
                            "timestamp": timestamp
                        },
                    )
                except Exception as e:
                    print(f"Error processing message: {str(e)}")
                    await self.send(text_data=json.dumps({
                        "type": "error",
                        "message": f"Failed to send message: {str(e)}"
                    }))
                    
            elif typing_status == "typing":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "user_typing", "username": username}
                )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Invalid message format"
            }))
        except Exception as e:
            print(f"Error in receive: {str(e)}")
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": f"An error occurred: {str(e)}"
            }))

    async def chat_message(self, event):
        """Send chat message to WebSocket."""
        try:
            await self.send(text_data=json.dumps({
                "type": "message",
                "message": event["message"],
                "username": event["username"],
                "timestamp": event["timestamp"]
            }))
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    async def user_typing(self, event):
        """Send typing indicator to WebSocket."""
        await self.send(text_data=json.dumps({
            "type": "typing",
            "username": event["username"]
        }))

    async def room_state_update(self, event):
        """Send room state update to WebSocket."""
        await self.send(text_data=json.dumps({
            "type": "room_state",
            "users": event["users"],
            "connection_count": event["connection_count"],
            "max_connections": event["max_connections"]
        }))
