from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tweet(models.Model):
    content = models.CharField(max_length=160)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.creation_date)

class Message(models.Model):
    message_from = models.ForeignKey(User)
    message_to = models.ForeignKey(User, related_name='UserTo')
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=256)
    seen = models.BooleanField(default=False)
