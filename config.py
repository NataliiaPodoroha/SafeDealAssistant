import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
API_KEY = os.getenv("SIMPLE_SWAP_API_KEY")
ADMIN_WALLET = os.getenv("ADMIN_WALLET_ADDRESS")
CURRENCY_TO = os.getenv("ADMIN_WALLET_CURRENCY")
