# messaging_app/chats/urls.py

from django.urls import path, include
# Import the nested router
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# The parent router for conversations
router = routers.SimpleRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# The nested router for messages.
# This creates URLs like /conversations/{conversation_pk}/messages/
conversations_router = routers.NestedDefaultRouter(
    router, 
    r'conversations', 
    lookup='conversation'
)
conversations_router.register(
    r'messages', 
    MessageViewSet, 
    basename='conversation-messages'
)

# The final urlpatterns will include both the parent and the nested routes.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]