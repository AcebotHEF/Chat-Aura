from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q

@login_required
def chat_home(request):
    # Sidebar: Show all users except the logged-in user
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/room.html', {'users': users})

@login_required
def chat_room(request, user_id):
    users = User.objects.exclude(id=request.user.id)
    other_user = get_object_or_404(User, id=user_id)
    
    # 1. Fetch History
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    # 2. GENERATE ROOM NAME: Ensure (1, 5) and (5, 1) become "chat_1_5"
    users_ids = [request.user.id, other_user.id]
    users_ids.sort() # Sorts to [1, 5]
    room_name = f"chat_{users_ids[0]}_{users_ids[1]}"

    return render(request, 'chat/room.html', {
        'users': users,
        'other_user': other_user,
        'messages': messages,
        'room_name': room_name # <--- We pass this specific room to the frontend
    })