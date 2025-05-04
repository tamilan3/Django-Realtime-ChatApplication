"""Video Call WebSocket consumers module.

This module contains the WebSocket consumer for handling real-time video call functionality,
including WebRTC signaling for peer-to-peer connections.
"""

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class VideoCallConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for video call signaling."""

    async def connect(self):
        """Handle new WebSocket connection for video calls."""
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"video_call_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handle incoming WebSocket messages for video call signaling.

        Processes WebRTC signaling messages including offers, answers, and ICE candidates.
        """
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

    async def _handle_offer(self, data):
        """Process and forward WebRTC offer."""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "video_offer",
                "offer": data["offer"],
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
                "sender_channel_name": self.channel_name,
            },
        )

    async def _handle_end(self, data):
        """Process and forward call end signal."""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "end_call",
                "sender_channel_name": self.channel_name,
            },
        )

    async def video_offer(self, event):
        """Send video offer to WebSocket."""
        if self.channel_name != event["sender_channel_name"]:
            await self.send(
                text_data=json.dumps({"type": "offer", "offer": event["offer"]})
            )

    async def video_answer(self, event):
        """Send video answer to WebSocket."""
        if self.channel_name != event["sender_channel_name"]:
            await self.send(
                text_data=json.dumps({"type": "answer", "answer": event["answer"]})
            )

    async def ice_candidate(self, event):
        """Send ICE candidate to WebSocket."""
        if self.channel_name != event["sender_channel_name"]:
            await self.send(
                text_data=json.dumps(
                    {"type": "ice_candidate", "candidate": event["candidate"]}
                )
            )

    async def end_call(self, event):
        """Send call end signal to WebSocket."""
        await self.send(text_data=json.dumps({"type": "end"}))
