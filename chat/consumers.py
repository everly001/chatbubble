from asyncio.windows_events import NULL
from concurrent.futures import thread
import json
from operator import contains
from tokenize import maybe
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Conversations
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import base64

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'
        
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    @database_sync_to_async
    def get_user_profile(self):
        return self.scope['user'].userprofile

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        if data['message_type'] == 'media':
            media = data['media']
            format, imgstr = media.split(';base64,') 
            ext = format.split('/')[-1] 

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        else:
            media = None
            data = None
        other_user_id = self.scope['url_route']['kwargs']['id']
        profile = await self.get_user_profile()
        profile_pic = profile.profile_picture.url

        await self.save_message(other_user_id, self.room_group_name, message, data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'media': media,
                'profile_pic': profile_pic,
            }
        )

    
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        media = event['media']
        profile_pic = event['profile_pic']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'media': media,
            'profile_pic': profile_pic,
        }))

    async def disconnect(self, close_code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )

    @database_sync_to_async
    def save_message(self, other_user_id, thread_name, message, data):
        conversation = Conversations.objects.get(thread_name=thread_name)
        receiver = User.objects.get(id=other_user_id)
        Message.objects.create(sender=self.scope['user'], receiver=receiver, message=message, media=data, conversation=conversation)