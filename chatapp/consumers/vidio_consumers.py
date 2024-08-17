"""
The `VideoCallConsumer` class is an asynchronous WebSocket consumer that handles the real-time communication for a video call feature in a chat application.

The consumer is responsible for the following:
- Joining and leaving a room group for the video call
- Handling incoming WebSocket messages of different types (offer, answer, ice_candidate, end)
- Forwarding the received messages to the appropriate room group members

The consumer uses the Django Channels library to manage the WebSocket connections and the group communication.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected to WebSocket")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'video_call_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']
        from icecream import ic
        ic(message_type)
        if message_type == 'offer':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'video_offer',
                    'offer': data['offer'],
                    'sender_channel_name': self.channel_name,
                }
            )
        elif message_type == 'answer':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'video_answer',
                    'answer': data['answer'],
                    'sender_channel_name': self.channel_name,
                }
            )
        elif message_type == 'ice_candidate':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ice_candidate',
                    'candidate': data['candidate'],
                    'sender_channel_name': self.channel_name,
                }
            )
        elif message_type == 'end':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'end_call',
                    'sender_channel_name': self.channel_name,
                }
            )

    async def video_offer(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': 'offer',
                'offer': event['offer']
            }))

    async def video_answer(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': 'answer',
                'answer': event['answer']
            }))

    async def ice_candidate(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': 'ice_candidate',
                'candidate': event['candidate']
            }))

    async def end_call(self, event):
        await self.send(text_data=json.dumps({
            'type': 'end'
        }))
