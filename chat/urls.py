from django.urls import path
from . import views

# NOTICE: It is plural "urlpatterns" with an "s" at the end!
urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
]