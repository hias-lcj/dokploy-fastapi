from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Primary DB
    DB_HOST = os.getenv("HOST")
    DB_USER = os.getenv("USER")
    DB_PASSWORD = os.getenv("PASSWORD")
    DB_DATABASE = os.getenv("DATABASE")
    DB_PORT = int(os.getenv("PORT", "3306"))

    # Secondary DB (new)
    NEW_DB_HOST = os.getenv("NEW_HOST", DB_HOST)
    NEW_DB_USER = os.getenv("NEW_USER", DB_USER)
    NEW_DB_PASSWORD = os.getenv("NEW_PASSWORD", DB_PASSWORD)
    NEW_DB_DATABASE = os.getenv("NEW_DATABASE", "newdb")
    NEW_DB_PORT = int(os.getenv("NEW_PORT", str(DB_PORT)))

    # LLM
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_API_BASE_URL = os.getenv('OPENAI_API_BASE_URL')
    LLM_MODEL = os.getenv('LLM_MODEL', 'Qwen/Qwen3-8B')

settings = Settings()
# print(settings)

