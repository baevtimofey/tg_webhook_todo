from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    NGROK_TUNNEL_URL = os.getenv("NGROK_TUNNEL_URL")

    WEBHOOK_PATH = f"/bot/{TELEGRAM_BOT_TOKEN}"
    WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}"


settings = Settings()
