from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "QRKot"
    description: str = "Благотворительный фонд поддержки котиков"
    # pytest пишет что только по умолчанию может пройти название:'sqlite+aiosqlite'
    database_url: str = "sqlite+aiosqlite"

    secret: str = "SECRET"

    class Config:
        env_file = ".env"


settings = Settings()
