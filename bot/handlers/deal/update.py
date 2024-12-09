from aiogram import Router
from aiogram.types import CallbackQuery

from database.db_setup import async_session
from database.models import Deal
from bot.keyboards.deal import change_status_keyboard

router = Router()


@router.callback_query(lambda c: c.data.startswith("change_status_"))
async def change_status(callback: CallbackQuery) -> None:
    deal_id = int(callback.data.split("_")[2])

    keyboard = change_status_keyboard(deal_id)
    await callback.message.edit_text(
        "Select a new status for the deal:", reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith("set_status_"))
async def set_status(callback: CallbackQuery) -> None:
    _, _, deal_id, status = callback.data.split("_")
    deal_id = int(deal_id)

    async with async_session() as session:
        deal = await session.get(Deal, deal_id)

        if not deal:
            await callback.message.edit_text("Deal not found.")
            return

        deal.status = status
        await session.commit()

    await callback.message.edit_text(
        f"Status of the deal has been updated to: {status}"
    )
