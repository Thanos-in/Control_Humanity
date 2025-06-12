from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        names = ", ".join([u.username for u in self.participants.all()])
        return f"ChatRoom: {names}"

class Message(models.Model):
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.timestamp}] {self.sender.username}: {self.content[:20]}"
