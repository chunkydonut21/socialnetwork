from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from chat.models import Chat, ChatMessage
import json
import datetime
from django.db.models import Q


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        """
        Connecting to the webscoket connection and creating a chat room if it doesn't exist
        """
        user_one = self.scope['user']
        user_two = User.objects.get(username=self.scope['url_route']['kwargs']['username'])

        chat = Chat.objects.get_queryset().filter(
            (Q(user1=user_one) and Q(user2=user_two)) | (Q(user1=user_two) and Q(user2=user_one)))
        if chat.exists():
            self.chat_obj = chat.first()
        else:
            self.chat_obj = Chat.objects.create(user1=user_one, user2=user_two)

        self.room_name = f'{self.chat_obj.id}'

        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def receive(self, text_data):

        """
        Receiving the message and sending to the users room
        """

        data = json.loads(text_data)

        message = json.dumps({
            'text': data["message"],
            'username': self.scope['user'].username
        })

        self.save_message(data["message"])

        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'send_message',
                'text': message
            }
        )

    def send_message(self, event):
        """
        Sending message back to the users
        """
        message = event['text']
        self.send(text_data=message)

    def disconnect(self, event):
        """
        Disconnecting the websocket connection
        """
        async_to_sync(self.channel_layer.group_discard(self.room_name, self.channel_name))

    def save_message(self, content):
        """
        Save chat message into the database
        """

        # saving message in the database
        ChatMessage.objects.create(chat=self.chat_obj, sender=self.scope['user'], content=content)
        chat = Chat.objects.get(id=self.chat_obj.id)
        chat.updated_at = datetime.datetime.now()

        chat.save()
