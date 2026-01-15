from fastapi import FastAPI, HTTPException
from app.services.deepl_service import DeepLService

app = FastAPI(title="Smart Translator API")

# Instanciamos el servicio
deepl_service = DeepLService()


@app.post("/translate")
async def translate_text(text: str, target_lang: str):
    # Llamamos al servicio (nota el await, ¡es asíncrono!)
    translated_text = await deepl_service.translate(text, target_lang)

    if translated_text is None:
        raise HTTPException(status_code=503, detail="Error al traducir con DeepL")

    return {
        "original": text,
        "translated": translated_text,
        "target_lang": target_lang
    }