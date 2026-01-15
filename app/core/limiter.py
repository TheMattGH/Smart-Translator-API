from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

if settings.REDIS_URL:
    storage_uri = settings.REDIS_URL
else:
    storage_uri = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
# Conectamos el limitador a nuestro Redis existente
# Si Redis falla, no bloqueamos la API (swallow_errors=True)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    strategy="fixed-window",
    swallow_errors=True
)