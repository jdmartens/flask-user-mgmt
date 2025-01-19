from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Config(BaseSettings):
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = 'us-east-1'
    S3_BUCKET: str
    COGNITO_USER_POOL_ID: str
    
    COGNITO_APP_CLIENT_ID: str
    COGNITO_APP_CLIENT_SECRET: str
    COGNITO_AUTHORITY: str
    COGNITO_META_URL: str

    FLASK_RUN_PORT: int

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Config()
