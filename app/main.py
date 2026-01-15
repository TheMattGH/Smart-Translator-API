from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

# Importamos la conexión a BD, Servicios y Repositorio
from app.db.session import get_db
from app.services.deepl_service import DeepLService
from app.services.cache_service import CacheService
from app.repositories.translation_repo import TranslationRepository

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter

app = FastAPI(title="Smart Translator API")

# Configuración de rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Instanciamos los servicios
deepl_service = DeepLService()
cache_service = CacheService()

@app.get("/")
def read_root():
    return {"status": "online", "message": "Smart Translator API is running 🚀"}
@app.post("/translate")
@limiter.limit("5/minute")
async def translate_text(
        request: Request,
        text: str,
        target_lang: str,
        db: AsyncSession = Depends(get_db)  # Inyectamos la sesión de BD aquí
):
    target_lang = target_lang.upper()
    text = text.strip()
    # VERIFICAR CACHÉ (REDIS)
    # Buscamos si ya tradujimos esto antes
    cached_text = await cache_service.get_translation(text, target_lang)

    if cached_text:
        return {
            "original": text,
            "translated": cached_text,
            "source": "CACHE (Redis) ⚡",
            "target_lang": target_lang
        }

    # CONSULTAR DEEPL (Si no estaba en caché)
    translated_text = await deepl_service.translate(text, target_lang)

    if not translated_text:
        raise HTTPException(status_code=503, detail="Error al conectar con DeepL")

    # GUARDAR EN CACHÉ (Para el futuro)
    await cache_service.set_translation(text, target_lang, translated_text)

    # GUARDAR EN BASE DE DATOS (Historial)
    repo = TranslationRepository(db)
    await repo.create(
        source_text=text,
        translated_text=translated_text,
        target_lang=target_lang
    )

    return {
        "original": text,
        "translated": translated_text,
        "source": "DEEPL API 🌍",
        "target_lang": target_lang
    }