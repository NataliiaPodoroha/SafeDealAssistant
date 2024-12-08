from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_panel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Create Product", callback_data="create_product"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Update Product", callback_data="update_product"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Delete Product", callback_data="delete_product"
                )
            ],
            [
                InlineKeyboardButton(
                    text="View Deals", callback_data="view_deals"
                )
            ],
        ]
    )
