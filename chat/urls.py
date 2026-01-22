from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),           # Empty screen
    path('<int:user_id>/', views.chat_room, name='chat_room'), # Specific chat
]