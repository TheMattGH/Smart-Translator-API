from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Definimos la URL base
storage_uri = settings.REDIS_URL if settings.REDIS_URL else f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"

# Definimos opciones extra para Render
storage_options = {}

if settings.REDIS_URL and "rediss://" in settings.REDIS_URL:
    # Si es una conexión segura (SSL), le decimos a Redis que no sea estricto con el certificado
    storage_options = {"ssl_cert_reqs": "none"}

print(f"🔌 Configurando Rate Limiter con: {storage_uri.split('?')[0]}")

print(f"🔌 Conectando Rate Limiter a: {storage_uri.split('?')[0]}...")
# Conectamos el limitador a nuestro Redis existente
# Si Redis falla, no bloqueamos la API (swallow_errors=True)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=storage_uri,
    storage_options=storage_options,
    strategy="fixed-window",
    swallow_errors=True
)