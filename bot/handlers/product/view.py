from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.future import select

from database.db_setup import async_session
from database.models import Product
from bot.keyboards.product import product_details_keyboard, product_list_keyboard

router = Router()


@router.message(Command("catalog"))
async def catalog(message: Message) -> None:
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

    if not products:
        await message.answer("Catalog is empty")
        return

    keyboard = product_list_keyboard(products)
    await message.answer("Catalog:", reply_markup=keyboard)


@router.callback_query(lambda callback: callback.data.startswith("product_"))
async def product_details(callback: CallbackQuery) -> None:
    product_id = int(callback.data.split("_")[1])

    async with async_session() as session:
        product = await session.get(Product, product_id)

    if not product:
        await callback.message.edit_text("Product not found.")
        return

    keyboard = product_details_keyboard()
    await callback.message.edit_text(
        f"🛒 **{product.name}**\n\n"
        f"💵 Price: {product.price} {product.currency}\n"
        f"📄 Description: {product.description}\n"
        f"👤 Seller: {product.seller}\n\n",
        reply_markup=keyboard,
    )


@router.callback_query(lambda callback: callback.data == "back_to_catalog")
async def back_to_catalog(callback: CallbackQuery) -> None:
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

    if not products:
        await callback.message.edit_text("Catalog is empty.")
        return

    keyboard = product_list_keyboard(products)
    await callback.message.edit_text("Catalog:", reply_markup=keyboard)
