import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import (
    start,
    catalog,
    admin,
    create_product,
    update_product,
    delete_product, deal, view_deals,
)
from aiogram.types import BotCommand
from database.db_setup import init_db
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)


async def create_bot():
    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(catalog.router)
    dp.include_router(admin.router)
    dp.include_router(deal.router)
    dp.include_router(view_deals.router)
    dp.include_router(create_product.router)
    dp.include_router(update_product.router)
    dp.include_router(delete_product.router)

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="catalog", description="Show catalog"),
            BotCommand(command="create_deal", description="Create a deal"),
            BotCommand(command="admin", description="Admin panel"),
        ]
    )

    return bot, dp
