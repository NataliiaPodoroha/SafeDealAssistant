import asyncio
from bot.main import create_bot


async def main():
    bot, dp = await create_bot()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
