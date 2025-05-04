"""Chat application models module.

This module defines the database models for chat rooms and messages.
"""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ChatRoom(models.Model):
    """Model representing a chat room.

    Attributes:
        name: The unique name of the chat room
    """

    name = models.CharField(
        max_length=100, unique=True, null=False, verbose_name="Room Name"
    )

    class Meta:
        """Model metadata."""

        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"
        ordering = ["name"]

    def __str__(self):
        """Return the room name as string representation."""
        return self.name


class ChatMessage(models.Model):
    """Model representing a chat message.

    Attributes:
        user: The user who sent the message
        room: The chat room the message belongs to
        message: The content of the message
        timestamp: When the message was sent
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, verbose_name="Sender"
    )
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Chat Room",
    )
    message = models.TextField(verbose_name="Message Content")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Sent At")

    class Meta:
        """Model metadata."""

        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
        ordering = ["-timestamp"]

    def __str__(self):
        """Return a string representation of the message."""
        return f"{self.user.username} in {self.room.name}: {self.message[:50]}"
