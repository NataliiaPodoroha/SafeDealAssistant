import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from bot.handlers import start, admin
from bot.handlers.deal import view as deal_view, create as deal_create
from bot.handlers.product import (
    delete as product_delete,
    create as product_create,
    update as product_update,
    view as product_view,
)
from aiogram.types import BotCommand


logging.basicConfig(level=logging.INFO)


async def create_bot():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(admin.router)

    # Include deal handlers
    dp.include_router(deal_create.router)
    dp.include_router(deal_view.router)

    # Include product handlers
    dp.include_router(product_view.router)
    dp.include_router(product_create.router)
    dp.include_router(product_update.router)
    dp.include_router(product_delete.router)

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="catalog", description="Show catalog"),
            BotCommand(command="create_deal", description="Create a deal"),
            BotCommand(command="admin", description="Admin panel"),
        ]
    )

    return bot, dp
