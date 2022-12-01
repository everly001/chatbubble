from django.contrib import admin
from .models import UserProfile, Conversations, Message

class MessageAdmin(admin.ModelAdmin):
    list_filter = ('sender', 'timestamp',)
    list_display = ('message', 'sender', 'timestamp',)

admin.site.register(UserProfile)
admin.site.register(Conversations)
admin.site.register(Message, MessageAdmin)

