import os.path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Calcula la ruta raíz del proyecto (sube 3 niveles desde este archivo)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Settings(BaseSettings):
    DEEPL_API_KEY: str
    DEEPL_URL: str = "https://api-free.deepl.com/v2/translate"

    DATABASE_URL: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()