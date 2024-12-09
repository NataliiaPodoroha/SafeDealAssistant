from aiogram.types import Message

from bot.keyboards.deal import confirm_deal_keyboard
import config
from database.models import Deal
from services.user_management import get_user_id_by_username


async def notify_second_party(message: Message, deal: Deal) -> None:
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


async def notify_parties_about_status_change(bot, deal: Deal, message: str) -> None:
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


async def notify_admin_about_confirmation(bot, deal: Deal) -> None:
    text = (
        f"🚨 New deal confirmed!\n\n"
        f"💵 Product: {deal.product_name}\n"
        f"💰 Amount: {deal.amount} {deal.currency}\n"
        f"👤 Buyer: @{deal.buyer}\n"
        f"👤 Seller: @{deal.seller}\n"
    )
    await bot.send_message(config.ADMIN_ID, text)
