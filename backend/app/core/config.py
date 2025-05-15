from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    database_url: str
    fernet_key: str

    class Config:
        env_file = ".env"

settings = Settings()
