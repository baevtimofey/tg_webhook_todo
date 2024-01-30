from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    NGROK_TUNNEL_URL = os.getenv("NGROK_TUNNEL_URL")

    WEBHOOK_PATH = f"/bot/{TELEGRAM_BOT_TOKEN}"
    WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}"

    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_DATABASE = os.getenv("DB_DATABASE")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    DB_ECHO = True

    API_V1_PREFIX = "/api/v1"


settings = Settings()
