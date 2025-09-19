from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):

    class Config:

        APP_NAME: str
        APP_VERSION: str
        OPENAI_API_KEY : str



        env_file = ".env"

def get_settings():
    return Settings()
