from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.future import select

from database.db_setup import async_session
from database.models import Deal
from bot.keyboards.deal import deal_list_keyboard, deal_details_keyboard


router = Router()


@router.callback_query(lambda c: c.data == "view_deals")
async def view_deals(callback: CallbackQuery) -> None:

    async with async_session() as session:
        result = await session.execute(select(Deal))
        deals = result.scalars().all()

    if not deals:
        await callback.message.edit_text("No deals available.")
        return

    keyboard = deal_list_keyboard(deals)
    await callback.message.edit_text("List of Deals:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("deal_"))
async def view_deal_details(callback: CallbackQuery) -> None:
    deal_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        deal = await session.get(Deal, deal_id)

    if not deal:
        await callback.message.edit_text("Deal not found.")
        return

    text = (
        f"**Deal Details**\n\n"
        f"Product: {deal.product_name}\n"
        f"Amount: {deal.amount} {deal.currency}\n"
        f"Buyer: @{deal.buyer}\n"
        f"Seller: @{deal.seller}\n"
        f"Status: {deal.status}\n"
    )

    keyboard = deal_details_keyboard(deal.id)
    await callback.message.edit_text(text, reply_markup=keyboard)


@router.callback_query(lambda callback: callback.data == "back_to_deals")
async def back_to_deals(callback: CallbackQuery) -> None:
    await view_deals(callback)
