from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/messages/(?P<username>[-:\w]+)/$', consumers.ChatConsumer.as_asgi()),
]