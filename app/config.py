from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "development"

    # MySQL Configuration
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "restaurant_db"

    db_cloud_sql_instance: str = ""

    deepseek_api_key: str = ""

    cors_origins: str = "http://localhost:4200"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def detected_db_type(self) -> str:
        return "mysql"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
