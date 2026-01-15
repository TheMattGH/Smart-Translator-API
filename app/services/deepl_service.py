import httpx
from app.core.config import settings


class DeepLService:
    def __init__(self):
        self.api_key = settings.DEEPL_API_KEY
        self.url = settings.DEEPL_URL

    async def translate(self, text: str, target_lang: str):
        """
        Envía una petición asíncrona a DeepL.
        """
        params = {
            "auth_key": self.api_key,
            "text": text,
            "target_lang": target_lang.upper(),  # DeepL espera 'ES', 'EN', etc.
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.url, data=params)
                response.raise_for_status()  # Lanza error si falla (404, 500, etc)

                data = response.json()
                # DeepL devuelve: {"translations": [{"text": "Hola", ...}]}
                return data["translations"][0]["text"]

            except httpx.HTTPStatusError as e:
                # Aquí podrías loguear el error real
                print(f"Error DeepL: {e.response.text}")
                return None
            except Exception as e:
                print(f"Error de conexión: {e}")
                return None