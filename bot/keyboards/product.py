from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.models import Product


def product_list_keyboard(products: list[Product]) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{product.name} - {product.price} {product.currency}",
                callback_data=f"product_{product.id}",
            )
        ]
        for product in products
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def product_details_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Back to catalog", callback_data="back_to_catalog")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def product_list_keyboard_for_updating(products: list[Product]) -> InlineKeyboardMarkup:
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


def product_list_keyboard_for_deletion(products: list[Product]) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{product.name} (ID: {product.id})",
                callback_data=f"delete_{product.id}",
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
