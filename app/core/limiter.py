from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

storage_uri = ""

if settings.REDIS_URL:
    storage_uri = settings.REDIS_URL
    # --- FIX PARA RENDER ---
    # Si la URL es segura (rediss://), añadimos el parámetro para saltar
    # la verificación estricta del certificado SSL, que suele fallar en planes free.
    if "rediss://" in storage_uri and "ssl_cert_reqs" not in storage_uri:
        storage_uri += "?ssl_cert_reqs=none"
    # -----------------------
else:
    storage_uri = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"

print(f"🔌 Conectando Rate Limiter a: {storage_uri.split('?')[0]}...")
# Conectamos el limitador a nuestro Redis existente
# Si Redis falla, no bloqueamos la API (swallow_errors=True)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    strategy="fixed-window",
    swallow_errors=True
)