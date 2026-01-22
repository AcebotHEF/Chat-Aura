import json
import asyncio
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth.models import User

# --- BOT PERSONALITIES ---
BOT_DATA = {
    "Grandma_Betty": {
        "vocab": ["Hello dear.", "Are you eating enough?", "That's nice.", "Love, Grandma.", "Back in my day...", "Oh my."]
    },
    "Zoomer_Jay": {
        "vocab": ["no cap", "bet", "bruh", "fr fr", "vibes", "rn", "slay", "lowkey", "💀"]
    },
    "Business_Bob": {
        "vocab": ["Please advise.", "Regards.", "Noted.", "I will circle back.", "Great synergy.", "Let's touch base."]
    },
    "Hype_Man": {
        "vocab": ["LETS GOOOO", "LIGHT WEIGHT BABY", "YEAHHH", "WOOOOO", "CANT STOP", "BEAST MODE"]
    },
    "Emoji_Emma": {
        "vocab": ["✨", "💖", "🥺", "omg", "literally so cute", "stop it", "🦋", "🌸"]
    }
}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"✅ Connection opened for room: {self.room_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print("❌ Connection closed")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            sender_username = data['sender']
            receiver_id = data['receiver_id']

            print(f"📩 Message received from {sender_username}: {message}")

            # 1. Save User's Message
            await self.save_message(sender_username, receiver_id, message)

            # 2. Broadcast User's Message
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender_username
                }
            )

            # 3. CHECK IF RECEIVER IS A BOT
            receiver_user = await self.get_user_by_id(receiver_id)
            print(f"🧐 Checking if receiver '{receiver_user.username}' is a bot...")

            if receiver_user.username in BOT_DATA:
                print(f"🤖 BOT DETECTED! Triggering reply for {receiver_user.username}...")
                await self.trigger_bot_reply(receiver_user, sender_username)
            else:
                print("👤 Receiver is a human. No bot reply needed.")

        except Exception as e:
            print(f"💥 ERROR in receive: {e}")

    async def trigger_bot_reply(self, bot_user, human_username):
        try:
            # A. Simulate typing time
            delay = random.uniform(0.5, 2)
            print(f"⏳ Bot is thinking for {delay:.2f} seconds...")
            await asyncio.sleep(delay)

            # B. Pick phrase
            personality = BOT_DATA[bot_user.username]
            bot_text = random.choice(personality['vocab'])

            # C. Save & Send
            human_user = await self.get_user_by_name(human_username)
            await self.save_message_direct(bot_user, human_user, bot_text)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': bot_text,
                    'sender': bot_user.username
                }
            )
            print(f"📤 BOT REPLIED: {bot_text}")
        except Exception as e:
             print(f"💥 ERROR in bot reply: {e}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    # --- DATABASE HELPERS ---
    @database_sync_to_async
    def save_message(self, sender_username, receiver_id, message):
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(id=receiver_id)
        Message.objects.create(sender=sender, receiver=receiver, content=message)

    @database_sync_to_async
    def save_message_direct(self, sender_obj, receiver_obj, message):
        Message.objects.create(sender=sender_obj, receiver=receiver_obj, content=message)

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_user_by_name(self, username):
        return User.objects.get(username=username)