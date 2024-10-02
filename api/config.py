import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_CONNECTION = os.getenv("DB_CONNECTION")

settings = Settings()
