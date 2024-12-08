from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import Deal


def deal_list_keyboard(deals: list[Deal]) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{deal.product_name} (Status: {deal.status})",
                callback_data=f"deal_{deal.id}",
            )
        ]
        for deal in deals
        if deal.status not in ["Completed", "Rejected"]
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Back to Admin Panel", callback_data="back_to_admin_panel"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def deal_details_keyboard(deal_id: int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Change Status", callback_data=f"change_status_{deal_id}"
            )
        ],
        [InlineKeyboardButton(text="Back to Deals", callback_data="back_to_deals")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def deal_type_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Buy", callback_data="buy")],
            [InlineKeyboardButton(text="Sell", callback_data="sell")],
        ]
    )


def confirm_deal_keyboard(deal_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Accept", callback_data=f"deal_accept_{deal_id}"
                ),
                InlineKeyboardButton(
                    text="Decline", callback_data=f"deal_decline_{deal_id}"
                ),
            ]
        ]
    )
