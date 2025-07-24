# messaging_app/messaging_app/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Your existing API routes
    path('api/', include('chats.urls')),
    
    # Add this line to include the DRF login/logout views.
    # This satisfies the "api-auth" check.
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]