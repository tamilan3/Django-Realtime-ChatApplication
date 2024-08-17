from django.db import models
from django.contrib.auth.models import User
from authapp.models import CustomUser
from django.conf import settings


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True,null=False)

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE,default=None)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.room.name}: {self.message}"



