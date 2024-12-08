from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from bot.keyboards.admin import admin_panel_keyboard
from config import ADMIN_ID

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("You are not authorized to access the admin panel.")
        return
    await message.reply("Welcome to Admin Panel", reply_markup=admin_panel_keyboard())


@router.callback_query(lambda callback: callback.data == "back_to_admin_panel")
async def back_to_admin_panel(callback: CallbackQuery):
    await callback.message.edit_text(
        "Welcome to the Admin Panel. Choose an option:",
        reply_markup=admin_panel_keyboard()
    )
