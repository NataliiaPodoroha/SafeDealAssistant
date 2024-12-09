import aiohttp
import certifi
import ssl
from config import SIMPLE_SWAP_API_KEY, ADMIN_WALLET, CURRENCY_TO

BASE_URL = "https://api.simpleswap.io/v1"


async def create_exchange(currency_from: str, amount: float) -> str:
    url = f"{BASE_URL}/create_exchange/"
    payload = {
        "fixed": False,
        "currency_from": currency_from,
        "currency_to": CURRENCY_TO,
        "amount": amount,
        "address_to": ADMIN_WALLET,
    }
    params = {
        "api_key": SIMPLE_SWAP_API_KEY,
    }

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, json=payload, params=params, ssl=ssl_context
        ) as response:
            if response.status != 200:
                raise Exception(f"SimpleSwap API error: {response.status}, {response.json()}")
            data = await response.json()

            payment_link = data.get("redirect_url")
            if not payment_link:
                raise Exception("Payment link not found in the response.")
            return payment_link
