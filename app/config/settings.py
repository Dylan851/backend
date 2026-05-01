from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    CORS_ORIGINS: str = ",".join([
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ])
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 10080  # 7 days
    GOOGLE_CLIENT_IDS: str = ""
    DIRECT_URL: str = ""  # For migrations, optional
    FRONTEND_URL: str = "http://localhost:8080"
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
