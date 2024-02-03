import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Base.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Configs.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Base.routing.websocket_urlpatterns
        )
    ),
})
