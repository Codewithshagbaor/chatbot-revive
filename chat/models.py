from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Room(models.Model):
    title = models.TextField()
    uid = models.CharField(max_length=20)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)

    def __str__(self):
        return self.uid

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    username = models.CharField(max_length=1000)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} - {self.content}"
