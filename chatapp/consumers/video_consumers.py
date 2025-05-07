"""Video Call WebSocket consumers module.

This module contains the WebSocket consumer for handling real-time video call functionality,
including WebRTC signaling for peer-to-peer connections.
"""

import json
from collections import defaultdict

from channels.generic.websocket import AsyncWebsocketConsumer


class VideoCallConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for video call signaling."""
    
    room_participants = {}  # Track participants in each room
    room_connections = defaultdict(int)  # Track number of connections per room
    MAX_ROOM_CONNECTIONS = 2  # Maximum connections for video calls (1-to-1)

    async def connect(self):
        """Handle new WebSocket connection for video calls."""
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"video_call_{self.room_name}"
        self.user = self.scope["user"]

        # Check room connection limit
        if self.room_connections[self.room_name] >= self.MAX_ROOM_CONNECTIONS:
            await self.close(code=4001)  # Custom close code for room full
            return

        # Initialize room if needed
        if self.room_name not in self.room_participants:
            self.room_participants[self.room_name] = set()

        # Add user and increment connection count
        self.room_participants[self.room_name].add(self.user.username)
        self.room_connections[self.room_name] += 1

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send room state update
        await self.send_room_state()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if hasattr(self, "user") and hasattr(self, "room_name"):
            if self.room_name in self.room_participants:
                self.room_participants[self.room_name].discard(self.user.username)
                self.room_connections[self.room_name] -= 1
                
                if self.room_connections[self.room_name] <= 0:
                    del self.room_participants[self.room_name]
                    del self.room_connections[self.room_name]
                
                await self.send_room_state()

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
        # Notify other participants about disconnection
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "peer_disconnected",
                "username": self.user.username
            }
        )

    async def send_room_state(self):
        """Send current room state to all participants."""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "room_state_update",
                "participants": list(self.room_participants.get(self.room_name, [])),
                "connection_count": self.room_connections.get(self.room_name, 0),
                "max_connections": self.MAX_ROOM_CONNECTIONS
            }
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages for video call signaling."""
        try:
            data = json.loads(text_data)
            message_type = data["type"]

            handlers = {
                "offer": self._handle_offer,
                "answer": self._handle_answer,
                "ice_candidate": self._handle_ice_candidate,
                "end": self._handle_end,
            }

            if handler := handlers.get(message_type):
                await handler(data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Invalid message format"
            }))

    async def _handle_offer(self, data):
        """Process and forward WebRTC offer."""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "video_offer",
                "offer": data["offer"],
                "sender": self.user.username,
                "sender_channel_name": self.channel_name,
            },
        )

    async def _handle_answer(self, data):
        """Process and forward WebRTC answer."""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "video_answer",
                "answer": data["answer"],
                "sender": self.user.username,
                "sender_channel_name": self.channel_name,
            },
        )

    async def _handle_ice_candidate(self, data):
        """Process and forward ICE candidate."""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "ice_candidate",
                "candidate": data["candidate"],
                "sender": self.user.username,
                "sender_channel_name": self.channel_name,
            },
        )

    async def _handle_end(self, data):
        """Process and forward call end signal."""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "end_call",
                "sender": self.user.username,
                "sender_channel_name": self.channel_name,
            },
        )

    async def video_offer(self, event):
        """Send video offer to WebSocket."""
        if self.channel_name != event["sender_channel_name"]:
            await self.send(text_data=json.dumps({
                "type": "offer",
                "offer": event["offer"],
                "sender": event["sender"]
            }))

    async def video_answer(self, event):
        """Send video answer to WebSocket."""
        if self.channel_name != event["sender_channel_name"]:
            await self.send(text_data=json.dumps({
                "type": "answer",
                "answer": event["answer"],
                "sender": event["sender"]
            }))

    async def ice_candidate(self, event):
        """Send ICE candidate to WebSocket."""
        if self.channel_name != event["sender_channel_name"]:
            await self.send(text_data=json.dumps({
                "type": "ice_candidate",
                "candidate": event["candidate"],
                "sender": event["sender"]
            }))

    async def end_call(self, event):
        """Send call end signal to WebSocket."""
        await self.send(text_data=json.dumps({
            "type": "end",
            "sender": event["sender"]
        }))

    async def peer_disconnected(self, event):
        """Handle peer disconnection notification."""
        await self.send(text_data=json.dumps({
            "type": "peer_disconnected",
            "username": event["username"]
        }))

    async def room_state_update(self, event):
        """Send room state update to WebSocket."""
        await self.send(text_data=json.dumps({
            "type": "room_state",
            "participants": event["participants"],
            "connection_count": event["connection_count"],
            "max_connections": event["max_connections"]
        }))
