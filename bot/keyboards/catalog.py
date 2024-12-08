from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models import Product


def catalog_keyboard(products: list[Product]) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{product.name} - {product.price} {product.currency}",
                callback_data=f"product_{product.id}"
            )
        ]
        for product in products
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def product_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Back to catalog",
                callback_data="back_to_catalog"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
