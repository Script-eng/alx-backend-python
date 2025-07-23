# messaging_app/chats/models.py

import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# --- User Model ---
# This model extends Django's built-in AbstractUser to add custom fields.
# We don't need to redefine first_name, last_name, email, or password,
# as AbstractUser already provides them.

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Specifies a UUID primary key and adds a phone number and role.
    """
    # Define roles using a choices tuple for the ENUM requirement.
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )

    # user_id (Primary Key, UUID)
    # We override the default integer 'id' with a UUID field.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # phone_number (VARCHAR, NULL)
    # blank=True allows the field to be empty in forms.
    # null=True allows the database to store a NULL value.
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # role (ENUM, NOT NULL)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    
    # created_at is handled by AbstractUser's 'date_joined' field automatically.

    def __str__(self):
        return self.username


# --- Conversation Model ---

class Conversation(models.Model):
    """
    Represents a conversation between two or more participants.
    """
    # conversation_id (Primary Key, UUID)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # participants_id (Foreign Key to User)
    # A ManyToManyField is the correct way to model a conversation where
    # multiple users can be participants.
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )

    # created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
    # auto_now_add=True sets the timestamp when the object is first created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# --- Message Model ---

class Message(models.Model):
    """
    Represents a single message within a conversation.
    """
    # message_id (Primary Key, UUID)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # sender_id (Foreign Key to User)
    # A message has one sender.
    # on_delete=models.CASCADE means if a user is deleted, their messages are too.
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    
    # This message must belong to a conversation.
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    # message_body (TEXT, NOT NULL)
    # TextField is used for long text content. It is NOT NULL by default.
    message_body = models.TextField()

    # sent_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Order messages by when they were sent by default.
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.sent_at.strftime('%Y-%m-%d %H:%M')}"