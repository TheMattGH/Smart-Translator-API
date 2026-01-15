from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.translation_log import TranslationLog

class TranslationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, source_text: str, translated_text: str, target_lang: str, source_lang: str = None):
        new_entry = TranslationLog(
            source_text=source_text,
            translated_text=translated_text,
            target_lang=target_lang,
            source_lang=source_lang
        )
        self.db.add(new_entry)
        await self.db.commit()
        await self.db.refresh(new_entry)
        return new_entry