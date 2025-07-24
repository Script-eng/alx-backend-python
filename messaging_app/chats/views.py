# messaging_app/chats/views.py

from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all conversations
        for the currently authenticated user.
        """
        # Filter conversations to only include those where the current user is a participant.
        return self.request.user.conversations.all()

    def perform_create(self, serializer):
        """
        Override to add the current user to the conversation's participants
        when a new conversation is created.
        """
        # The serializer validated_data for 'participants' will be a list of User objects.
        participants = serializer.validated_data.get('participants')
        
        # Ensure the creator is always a participant.
        if self.request.user not in participants:
            participants.append(self.request.user)
        
        serializer.save(participants=participants)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or created.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all messages in conversations
        that the current user is a part of.
        """
        # First, get all conversations the user is a part of.
        user_conversations = self.request.user.conversations.all()
        # Then, filter messages to only those belonging to these conversations.
        return Message.objects.filter(conversation__in=user_conversations)

    def perform_create(self, serializer):
        """
        Override to automatically set the sender of the message
        to the currently authenticated user. This is a crucial security measure.
        """
        # The frontend only needs to provide the conversation_id and message_body.
        # The sender is securely set on the backend.
        serializer.save(sender=self.request.user)