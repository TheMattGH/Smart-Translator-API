from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.db.session import Base

class TranslationLog(Base):
    __tablename__ = "translation_logs"

    id = Column(Integer, primary_key=True, index=True)
    source_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_lang = Column(String(10), nullable=True) # Ej: "EN"
    target_lang = Column(String(10), nullable=False) # Ej: "ES"
    created_at = Column(DateTime, default=datetime.utcnow)