# Generated by Django 4.1 on 2022-08-11 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0003_alter_conversation_participants"),
    ]

    operations = [
        migrations.RemoveField(model_name="conversation", name="participants",),
    ]
