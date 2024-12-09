from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards.deal import deal_type_keyboard
from database.db_setup import async_session
from database.models import Deal, DealStatus
from services.notifications import (
    notify_second_party,
    notify_parties_about_status_change,
    notify_admin_about_confirmation,
)
from services.simpleswap import create_exchange
from services.user_management import get_user_id_by_username

router = Router()


class DealForm(StatesGroup):
    choose_type = State()
    get_details = State()


@router.message(Command("create_deal"))
async def start_create_deal(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Do you want to buy or sell a product?",
        reply_markup=deal_type_keyboard(),
    )
    await state.set_state(DealForm.choose_type)


@router.callback_query(lambda c: c.data in ["buy", "sell"])
async def set_deal_type(callback: CallbackQuery, state: FSMContext) -> None:
    deal_type = "buyer" if callback.data == "buy" else "seller"
    await state.update_data(deal_type=deal_type)
    await callback.message.edit_text(
        "Enter details in the format:\n"
        "`Product Name|Amount|Currency|Other Party Username`"
    )
    await state.set_state(DealForm.get_details)


@router.message(DealForm.get_details)
async def save_deal(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    deal_type = user_data["deal_type"]
    details = message.text.split("|")

    if len(details) != 4:
        await message.reply(
            "Invalid format. Please use:\n"
            "`Product Name|Amount|Currency|Other Party Username`"
        )
        return

    product_name, amount, currency, other_party = details

    if deal_type == "buyer":
        buyer, seller = message.from_user.username, other_party
    else:
        buyer, seller = other_party, message.from_user.username

    async with async_session() as session:
        new_deal = Deal(
            buyer=buyer,
            seller=seller,
            product_name=product_name,
            amount=float(amount),
            currency=currency.upper(),
            status=DealStatus.NEW,
        )
        session.add(new_deal)
        await session.commit()

    await notify_second_party(message, new_deal)

    await state.clear()
    await message.answer(
        f"Deal created successfully:\n"
        f"Product: {product_name}\n"
        f"Buyer: @{buyer}\n"
        f"Seller: @{seller}\n"
        f"Amount: {amount} {currency}\n"
        f"Status: New"
    )


@router.callback_query(lambda callback: callback.data.startswith("deal_accept_"))
async def accept_deal(callback: CallbackQuery) -> None:
    deal_id = int(callback.data.split("_")[2])

    async with async_session() as session:
        deal = await session.get(Deal, deal_id)
        if not deal:
            await callback.message.edit_text("Deal not found.")
            return

        if deal.status != DealStatus.NEW:
            await callback.message.edit_text("This deal cannot be accepted.")
            return

        try:
            payment_link = await create_exchange(
                currency_from=deal.currency, amount=deal.amount
            )
            deal.payment_link = payment_link
        except Exception:
            await callback.message.edit_text("Error generating payment link.")
            return

        deal.status = DealStatus.ACCEPTED
        await session.commit()

        buyer_id = await get_user_id_by_username(deal.buyer)
        if buyer_id:
            await callback.bot.send_message(
                buyer_id,
                f"✅ Your deal has been confirmed!\n\n"
                f"💵 Product: {deal.product_name}\n"
                f"🔗 Payment link: [Pay now]({payment_link})",
                parse_mode="Markdown",
            )

    await notify_admin_about_confirmation(callback.bot, deal)

    await callback.message.edit_text("You have accepted the deal.")


@router.callback_query(lambda c: c.data.startswith("deal_decline_"))
async def decline_deal(callback: CallbackQuery) -> None:
    deal_id = int(callback.data.split("_")[2])

    async with async_session() as session:
        deal = await session.get(Deal, deal_id)

        if not deal:
            await callback.message.edit_text("Deal not found.")
            return

        if deal.status != DealStatus.NEW:
            await callback.message.edit_text(
                f"This deal is already processed (Status: {deal.status.name})."
            )
            return

        deal.status = DealStatus.REJECTED
        await session.commit()

    await notify_parties_about_status_change(
        callback.bot, deal, "The deal has been declined."
    )

    await callback.message.edit_text("You have declined the deal.")
