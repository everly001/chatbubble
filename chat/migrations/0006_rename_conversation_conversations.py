# Generated by Django 4.1 on 2022-08-12 10:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat", "0005_conversation_participant_1_and_more"),
    ]

    operations = [
        migrations.RenameModel(old_name="Conversation", new_name="Conversations",),
    ]
