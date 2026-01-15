from slowapi import Limiter
from slowapi.util import get_remote_address
import redis
from app.core.config import settings

# Conectamos el limitador a nuestro Redis existente
# Si Redis falla, no bloqueamos la API (swallow_errors=True)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    strategy="fixed-window",
    swallow_errors=True
)