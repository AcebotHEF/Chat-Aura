from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # <--- Import this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    
    # Add this line to redirect the empty path '' to the chat lobby
    path('', RedirectView.as_view(url='chat/')), 
]
