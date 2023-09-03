from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "QRKot"
    description: str = "Благотворительный фонд поддержки котиков"
    # pytest просит по дефолту поставить : sqlite+aiosqlite
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"

    secret: str = "SECRET"

    class Config:
        env_file = ".env"


settings = Settings()
