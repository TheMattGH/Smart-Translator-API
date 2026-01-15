from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DEEPL_API_KEY: str
    DEEPL_URL: str = "https://api-free.deepl.com/v2/translate"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()