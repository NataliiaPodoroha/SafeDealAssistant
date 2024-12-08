from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.future import select

from bot.keyboards.deals import deal_list_keyboard, deal_details_keyboard
from database.models import Deal, DealStatus
from database.db_setup import async_session


router = Router()


@router.callback_query(lambda c: c.data == "view_deals")
async def view_deals(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(select(Deal))
        deals = result.scalars().all()

    if not deals:
        await callback.message.edit_text("No deals available.")
        return

    keyboard = deal_list_keyboard(deals)
    await callback.message.edit_text("List of Deals:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("deal_"))
async def view_deal_details(callback: CallbackQuery):
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


@router.callback_query(lambda c: c.data.startswith("change_status_"))
async def change_status(callback: CallbackQuery):
    deal_id = int(callback.data.split("_")[2])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="New", callback_data=f"set_status_{deal_id}_{DealStatus.NEW}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Accepted", callback_data=f"set_status_{deal_id}_{DealStatus.ACCEPTED}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Rejected", callback_data=f"set_status_{deal_id}_{DealStatus.REJECTED}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Completed", callback_data=f"set_status_{deal_id}_{DealStatus.COMPLETED}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Back to Deal", callback_data=f"deal_{deal_id}"
                )
            ],
        ]
    )
    await callback.message.edit_text(
        "Select a new status for the deal:", reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith("set_status_"))
async def set_status(callback: CallbackQuery):
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


@router.callback_query(lambda callback: callback.data == "back_to_deals")
async def back_to_deals(callback: CallbackQuery):
    await view_deals(callback)
