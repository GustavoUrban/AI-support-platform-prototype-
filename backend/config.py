import os


class Settings:
    """
    Config simples para manter o projeto fácil de estudar.
    """
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    cors_origins: list[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:5500,http://localhost:5500",
    ).split(",")


settings = Settings()
