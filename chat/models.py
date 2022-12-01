from cgitb import text
from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache 
import datetime
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg')
    last_seen = models.DateTimeField()
    is_online = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def is_online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                        seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False 

class Conversations(models.Model):
    participant_1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant_1', null=True)
    participant_2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant_2', null=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return f'{self.participant_1}-{self.participant_2}'

class Message(models.Model):
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    media = models.FileField(upload_to='chat_media', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_unread = models.BooleanField(default=True)

    def __str__(self):
        return self.message
 
    class Meta:
        ordering = ('-timestamp',)