"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import django
import os
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from data_sync import consumers as sender_consumer
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()


websocket_urlpatterns = [
    re_path(r'ws/sender-socket/',
            sender_consumer.DataSyncSenderConsumer.as_asgi()),

]

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            AllowedHostsOriginValidator(
                URLRouter(
                    websocket_urlpatterns
                )
            ))

    }
)
