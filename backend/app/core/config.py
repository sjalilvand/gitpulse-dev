from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "GitPulse AI"
    secret_key: str = "your-secret-key-change-this"
    environment: str = "development"
    debug: bool = True

    # Database
    database_url: str = "postgresql://gitpulse:gitpulse123@postgres:5432/gitpulse"
    clickhouse_url: str = "http://clickhouse:8123"
    clickhouse_user: str = "default"
    clickhouse_password: str = "clickhouse123"
    clickhouse_db: str = "gitpulse_analytics"

    # Kafka
    kafka_bootstrap_servers: str = "kafka:29092"

    # GitHub
    github_token: str = ""

    # AI - Avalai
    avalai_api_key: str = ""
    avalai_base_url: str = "https://api.avalai.ir/v1"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()