from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    telegram_bot_token: str
    telegram_webhook_secret: str
    app_base_url: str
    database_url: str
    environment: str = "development"
    admin_telegram_ids: str = ""
    timezone: str = "UTC"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def admin_ids_list(self) -> List[int]:
        if not self.admin_telegram_ids:
            return []
        return [int(x.strip()) for x in self.admin_telegram_ids.split(",") if x.strip().isdigit()]

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

settings = Settings()
