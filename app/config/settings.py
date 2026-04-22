import json

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080,http://127.0.0.1:8080"
    FRONTEND_URL: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 10080  # 7 days
    DIRECT_URL: str = ""  # For migrations, optional
    AUTO_CREATE_TABLES: bool = False  # Set True once for first deploy if DB is empty

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def get_cors_origins(self) -> list[str]:
        raw_value = self.CORS_ORIGINS.strip()

        if raw_value.startswith("["):
            try:
                origins = json.loads(raw_value)
                if isinstance(origins, list):
                    parsed = [str(origin).strip() for origin in origins if str(origin).strip()]
                else:
                    parsed = []
            except json.JSONDecodeError:
                parsed = []
        else:
            parsed = [origin.strip() for origin in raw_value.split(",") if origin.strip()]

        if self.FRONTEND_URL.strip():
            parsed.append(self.FRONTEND_URL.strip())

        # Remove duplicates while preserving order
        deduped = list(dict.fromkeys(parsed))
        return deduped or ["*"]


settings = Settings()
