import os
import django
import random

# 1. Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mychat.settings')
django.setup()

from django.contrib.auth.models import User
from chat.models import Message

# 2. Define Personalities
BOTS = [
    {
        "name": "Grandma_Betty",
        "style": "old",
        "vocab": ["Dear,", "Hello dear.", "Hope you are eating well.", "Love, Grandma.", "The weather is nice.", "How is school?"]
    },
    {
        "name": "Zoomer_Jay",
        "style": "genz",
        "vocab": ["fr", "no cap", "bet", "bruh", "im dead 💀", "vibes", "rn", "slay", "lowkey"]
    },
    {
        "name": "Business_Bob",
        "style": "formal",
        "vocab": ["Please advise.", "Regards,", "Per our last email.", "Touching base.", "Synergy.", "Action items."]
    },
    {
        "name": "Hype_Man",
        "style": "hype",
        "vocab": ["LETS GOOOO", "YEA BUDDY", "LIGHT WEIGHT BABY", "WOOOOO", "CANT STOP WONT STOP", "🔥", "💪"]
    },
    {
        "name": "Emoji_Emma",
        "style": "emoji",
        "vocab": ["✨", "💖", "🌸", "🥺", "Did you see this??", "OMG", "So cute", "🦋"]
    }
]

def generate_text(style, vocab):
    """Generates a message based on personality"""
    length = random.randint(1, 3)
    words = random.sample(vocab, length)
    
    if style == "old":
        return f"{words[0]} {words[-1]}"
    elif style == "genz":
        return " ".join(words).lower()
    elif style == "hype":
        return " ".join(words).upper() + "!!!"
    elif style == "emoji":
        return f"{words[0]} {words[-1]} ✨"
    else: # formal
        return f"{words[0]} {words[-1]}"

# 3. Create Users and Fake History
def populate():
    print("🤖 Waking up the bots...")
    
    # Get your main user (Assuming ID 1 is you)
    try:
        me = User.objects.get(id=1)
    except User.DoesNotExist:
        print("❌ Error: You need to create your own Superuser first!")
        return

    for bot_data in BOTS:
        # Create User if not exists
        username = bot_data['name']
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password("password123")
            user.save()
            print(f"✅ Created bot: {username}")
        else:
            print(f"🔹 Found bot: {username}")

        # Create 3-5 random messages history
        print(f"   Writing fake messages for {username}...")
        for _ in range(random.randint(3, 5)):
            # Randomly decide if THEY sent it or YOU sent it
            if random.choice([True, False]):
                sender = user
                receiver = me
            else:
                sender = me
                receiver = user
            
            # Generate text
            content = generate_text(bot_data['style'], bot_data['vocab'])
            
            Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content
            )

    print("\n🎉 DONE! Go refresh your browser.")

if __name__ == '__main__':
    populate()