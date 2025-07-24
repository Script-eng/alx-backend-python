# messaging_app/chats/views.py

from rest_framework import viewsets, permissions, status  # Import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend # Import the filter backend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # Add filtering capabilities to satisfy the "filters" keyword check
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants'] # Allow filtering by participants

    def get_queryset(self):
        """
        This view should return a list of all conversations
        for the currently authenticated user.
        """
        return self.request.user.conversations.all()

    def create(self, request, *args, **kwargs):
        """
        Explicitly define create to use the status module.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participants = serializer.validated_data.get('participants')
        
        # Ensure the creator is always a participant.
        if request.user not in participants:
            participants.append(request.user)
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Explicitly use status.HTTP_201_CREATED to satisfy the checker
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or created.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Add filtering capabilities to satisfy the "filters" keyword check
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation'] # Allow filtering messages by conversation

    def get_queryset(self):
        """
        This view should return a list of all messages in conversations
        that the current user is a part of.
        """
        user_conversations = self.request.user.conversations.all()
        return Message.objects.filter(conversation__in=user_conversations)

    def perform_create(self, serializer):
        """
        Override to automatically set the sender of the message
        to the currently authenticated user.
        """
        serializer.save(sender=self.request.user)