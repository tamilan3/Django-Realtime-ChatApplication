"""ASGI config for chatproject project.

This module contains the ASGI application configuration for handling both HTTP and WebSocket
protocols using Django Channels. It sets up the routing for both protocols and includes
authentication middleware for WebSocket connections.
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chatapp.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatproject.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(chatapp.routing.websocket_urlpatterns)
        ),
    }
)
