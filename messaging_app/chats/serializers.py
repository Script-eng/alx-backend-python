# messaging_app/chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message

# It's good practice to define serializers from least dependent to most dependent.
# User -> Message -> Conversation

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Handles user creation with password hashing.
    """
    class Meta:
        model = User
        # List the fields you want to expose in the API.
        # It's crucial to EXCLUDE the password hash from being read.
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password']
        # Use extra_kwargs to make the password write-only.
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Override the create method to use Django's `create_user` helper,
        which correctly handles password hashing.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', None),
            role=validated_data.get('role', 'guest')
        )
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Displays the sender's username for readability.
    """
    # Use StringRelatedField to display the user's string representation (username)
    # This is more efficient than nesting a full UserSerializer here.
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        # Include all fields from the model.
        fields = ['id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    This is the detailed view that includes nested participants and messages.
    """
    # Nest the UserSerializer to show full participant details.
    # many=True is required for a many-to-many relationship.
    participants = UserSerializer(many=True, read_only=True)

    # Nest the MessageSerializer to show all messages within the conversation.
    # We use the 'related_name' from the Message model's ForeignKey ('messages').
    # many=True is required because one conversation has many messages.
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        # Define the fields to include in the final output.
        fields = ['id', 'participants', 'created_at', 'messages']