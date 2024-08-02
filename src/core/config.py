from pydantic_settings import BaseSettings, SettingsConfigDict


class __Config(BaseSettings):
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    jwt_algorithm: str
    jwt_access_secret_key: str
    jwt_access_expire_minutes: int
    jwt_refresh_secret_key: str
    jwt_refresh_expire_minutes: int
    riot_api_key: str

    model_config = SettingsConfigDict(env_file=".env")


config = __Config()
