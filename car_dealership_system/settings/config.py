from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Base(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv(), extra="ignore")


class Django(Base):
    SECRET_KEY: str
    DEBUG: bool
    ALLOWED_HOSTS: str


class JWT(Base):
    SIGNING_KEY: str
    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int

    EMAIL_VERIFY_TOKEN_LIFETIME: int
    ACTION_TOKEN_LIFETIME: int


class DataBase(Base):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str


class Redis(Base):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_PASS: str

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"


class Config(Base):
    django: Django = Django()  # type: ignore
    jwt: JWT = JWT()  # type: ignore
    database: DataBase = DataBase()  # type: ignore
    redis: Redis = Redis()  # type: ignore


config = Config()
