from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Importamos la conexión a BD, Servicios y Repositorio
from app.db.session import get_db
from app.services.deepl_service import DeepLService
from app.services.cache_service import CacheService
from app.repositories.translation_repo import TranslationRepository

app = FastAPI(title="Smart Translator API")

# Instanciamos los servicios
deepl_service = DeepLService()
cache_service = CacheService()


@app.post("/translate")
async def translate_text(
        text: str,
        target_lang: str,
        db: AsyncSession = Depends(get_db)  # Inyectamos la sesión de BD aquí
):
    # VERIFICAR CACHÉ (REDIS)
    # Buscamos si ya tradujimos esto antes
    cached_text = await cache_service.get_translation(text, target_lang)

    if cached_text:
        return {
            "original": text,
            "translated": cached_text,
            "source": "CACHE (Redis) ⚡",  # <--- ESTO ES LO QUE TE FALTABA
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