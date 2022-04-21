from pydantic import BaseSettings


class ApiConfig(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire: int

    class Config:
        env_file = ".env"
        env_prefix = "api_"


api_config = ApiConfig()
