from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    redis_host: str = "localhost"
    redis_port: int
    redis_password: str | None = None
    webhook_url: str
    webhook_secret: str
    admin_id: int
    database_url: str
    
    # загружать из env
    model_config = {"env_file": ".env"}

settings = Settings()