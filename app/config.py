import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MODELO: str = os.getenv("MODELO", "deepseek-r1")


settings = Settings()