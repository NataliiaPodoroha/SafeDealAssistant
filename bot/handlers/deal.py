from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.keyboards.deals import deal_type_keyboard, confirm_deal_keyboard
from config import ADMIN_ID
from services.simpleswap import create_exchange
from database.db_setup import async_session
from database.models import Deal, DealStatus
from database.user_management import get_user_id_by_username

router = Router()


class DealForm(StatesGroup):
    choose_type = State()
    get_details = State()


@router.message(Command("create_deal"))
async def start_create_deal(message: Message, state: FSMContext):
    await message.answer(
        "Do you want to buy or sell a product?", reply_markup=deal_type_keyboard()
    )
    await state.set_state(DealForm.choose_type)


@router.callback_query(lambda c: c.data in ["buy", "sell"])
async def set_deal_type(callback: CallbackQuery, state: FSMContext):
    deal_type = "buyer" if callback.data == "buy" else "seller"
    await state.update_data(deal_type=deal_type)
    await callback.message.edit_text(
        "Enter details in the format:\n`Product Name|Amount|Currency|Other Party Username`"
    )
    await state.set_state(DealForm.get_details)


@router.message(DealForm.get_details)
async def save_deal(message: Message, state: FSMContext):
    user_data = await state.get_data()
    deal_type = user_data["deal_type"]
    details = message.text.split("|")

    if len(details) != 4:
        await message.reply(
            "Invalid format. Please use:\n`Product Name|Amount|Currency|Other Party Username`"
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


async def notify_second_party(message: Message, deal: Deal):
    recipient_nick = (
        deal.seller if deal.buyer == message.from_user.username else deal.buyer
    )
    recipient_user_id = await get_user_id_by_username(recipient_nick)

    if not recipient_user_id:
        await message.answer(f"Error: Could not find user @{recipient_nick}.")
        return

    text = (
        f"New deal request!\n\n"
        f"Product: {deal.product_name}\n"
        f"Amount: {deal.amount} {deal.currency}\n"
        f"Buyer: @{deal.buyer}\n"
        f"Seller: @{deal.seller}\n\n"
        "Do you accept this deal?"
    )
    await message.bot.send_message(
        recipient_user_id, text, reply_markup=confirm_deal_keyboard(deal.id)
    )


@router.callback_query(lambda callback: callback.data.startswith("deal_accept_"))
async def accept_deal(callback: CallbackQuery):
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
        except Exception as e:
            print(e)
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
async def decline_deal(callback: CallbackQuery):
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


async def notify_parties_about_status_change(bot, deal: Deal, message: str):
    buyer_id = await get_user_id_by_username(deal.buyer)
    seller_id = await get_user_id_by_username(deal.seller)

    notification_text = f"Deal Update: {message}\n\n{format_deal_details(deal)}"

    if buyer_id:
        await bot.send_message(buyer_id, notification_text)

    if seller_id:
        await bot.send_message(seller_id, notification_text)


def format_deal_details(deal: Deal) -> str:
    return (
        f"Product: {deal.product_name}\n"
        f"Amount: {deal.amount} {deal.currency}\n"
        f"Buyer: @{deal.buyer}\n"
        f"Seller: @{deal.seller}\n"
        f"Status: {deal.status}"
    )


async def notify_admin_about_confirmation(bot, deal: Deal):
    text = (
        f"🚨 New deal confirmed!\n\n"
        f"💵 Product: {deal.product_name}\n"
        f"💰 Amount: {deal.amount} {deal.currency}\n"
        f"👤 Buyer: @{deal.buyer}\n"
        f"👤 Seller: @{deal.seller}\n"
    )
    await bot.send_message(ADMIN_ID, text)
