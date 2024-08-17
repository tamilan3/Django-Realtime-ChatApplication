import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ..models import ChatMessage, ChatRoom
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        username = text_data_json.get('username')
        typing_status = text_data_json.get('typing')
        room_name = self.room_name

        if message:
            try:
                user = await sync_to_async(User.objects.get)(username=username)
                room, created = await sync_to_async(ChatRoom.objects.get_or_create)(name=room_name)
                chat_message = ChatMessage(user=user, room=room, message=message)
                await sync_to_async(chat_message.save)()

            except User.DoesNotExist:
                # Handle the case where the user does not exist
                pass
            except ChatRoom.DoesNotExist:
                # Handle the case where the room does not exist
                pass
            except Exception as e:
                # Handle other exceptions
                print(e)
            finally:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': username
                    }
                )
        elif typing_status == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_typing',
                    'username': username
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def user_typing(self, event):
        type = event['type']
        username = event["username"]
    
        await self.send(text_data=json.dumps({
            'typing': True,
            'username': username
        }))


