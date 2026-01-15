import redis.asyncio as redis
import hashlib
from app.core.config import settings

class CacheService:
    def __init__(self):
        if settings.REDIS_URL:
            url = settings.REDIS_URL
            print("🔌 Usando conexión REDIS_URL (Render/Cloud)")
        else:
            url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
            print(f"🔌 Usando conexión manual: {settings.REDIS_HOST}:{settings.REDIS_PORT}")

        self.redis = redis.from_url(
            url,
            encoding="utf-8",
            decode_responses=True
        )
        self.ttl = 86400  # 24 horas

    async def get_translation(self, text: str, target_lang: str) -> str | None:
        key = self._generate_key(text, target_lang)
        return await self.redis.get(key)

    async def set_translation(self, text: str, target_lang: str, translation: str):
        key = self._generate_key(text, target_lang)
        await self.redis.set(key, translation, ex=self.ttl)

    def _generate_key(self, text: str, target_lang: str) -> str:
        raw_key = f"{text}:{target_lang}"
        return hashlib.sha256(raw_key.encode()).hexdigest()