from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def product_list_keyboard(products):
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{product.name} (ID: {product.id})",
                callback_data=f"update_{product.id}",
            )
        ]
        for product in products
    ]
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Back to Admin Panel", callback_data="back_to_admin_panel"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
