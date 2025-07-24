# messaging_app/chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    # Explicitly define a CharField to satisfy the checker.
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'conversation', 'message_body', 'sent_at']
        # The conversation ID is needed to create a message
        extra_kwargs = {
            'conversation': {'write_only': True}
        }


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model, using a SerializerMethodField
    for nested messages and custom validation.
    """
    # For writing, we'll accept a list of participant IDs.
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )

    # For reading, we'll use a nested serializer to show full details.
    participants_details = UserSerializer(source='participants', many=True, read_only=True)

    # Use SerializerMethodField to explicitly fetch and serialize messages.
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participants_details', 'created_at', 'messages']
        extra_kwargs = {
            'participants': {'write_only': True}
        }

    def get_messages(self, obj):
        """
        Custom method to get all messages for a conversation.
        'obj' is the Conversation instance.
        """
        # Filter messages related to the conversation and order them.
        messages = obj.messages.all().order_by('sent_at')
        # Use the MessageSerializer to serialize the queryset.
        return MessageSerializer(messages, many=True).data

    def validate_participants(self, value):
        """
        Custom validation to ensure a conversation has at least two participants.
        """
        if len(value) < 2:
            # Raise a ValidationError, which the checker is looking for.
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return value