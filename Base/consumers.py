import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from chat.models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_uid = self.scope['url_route']['kwargs']['room_uid']
        self.room_group_name = f'chat_{self.room_uid}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Check if the client is requesting previous messages
        query_string = self.scope['query_string'].decode('utf-8')
        if 'get_previous_messages' in query_string:
            await self.send_previous_messages()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def get_room(self):
        return Room.objects.get(uid=self.room_uid)

    @sync_to_async
    def get_previous_messages(self, room):
        # Retrieve previous messages from the database
        return Message.objects.filter(room=room).values('username', 'content')

    @sync_to_async
    def create_message(self, room, content, username):
        return Message.objects.create(room=room, content=content, username=username)

    async def chat_message(self, event):
        content = event['content']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'content': content,
            'username': username,
        }))

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            content = data['content']
            username = data['username']
        except KeyError:
            # Handle the case where 'content' key is missing
            return

        # Perform the database operation using sync_to_async
        room = await self.get_room()
        user = self.scope["user"]

        # Save message to the database
        await self.create_message(room=room, content=content, username=username)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'content': content,
                'username': user.username,
            }
        )


    async def send_previous_messages(self):
        # Retrieve previous messages
        room = await self.get_room()
        previous_messages = await self.get_previous_messages(room)

        # Use sync_to_async to convert the synchronous list() operation to asynchronous
        previous_messages_list = await sync_to_async(list)(previous_messages)

        # Send previous messages to the client
        await self.send(text_data=json.dumps({
            'type': 'previous.messages',
            'previous_messages': previous_messages_list,
        }))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'public_room'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({ 'message': event['message'] }))