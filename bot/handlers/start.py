from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select

from database.db_setup import async_session
from database.models import User


router = Router()


async def register_user(user_id: int, username: str):
    async with async_session() as session:
        existing_user = await session.execute(
            select(User).where(User.telegram_id == user_id)
        )
        if existing_user.scalar():
            return

        new_user = User(
            telegram_id=user_id,
            username=username or "unknown",
        )
        session.add(new_user)
        await session.commit()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    await register_user(
        user_id=user_id,
        username=username,
    )
    await message.answer(
        "👋 **Hello and welcome!**\n"
        "I'm here to help you with secure transactions.\n"
        "Let's get started!",
        parse_mode="Markdown",
    )
