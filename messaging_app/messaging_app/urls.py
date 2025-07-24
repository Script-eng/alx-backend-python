# messaging_app/messaging_app/urls.py

from django.contrib import admin
from django.urls import path, include  # Make sure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Add this line to include the URLs from your 'chats' app
    path('api/', include('chats.urls')),
]