import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "olympiad.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

import django
django.setup()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
