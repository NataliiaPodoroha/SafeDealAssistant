from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.future import select

from bot.keyboards.product import product_list_keyboard_for_deletion
from database.models import Product
from database.db_setup import async_session

router = Router()


@router.callback_query(lambda c: c.data == "delete_product")
async def list_products_for_deletion(callback: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

    if not products:
        await callback.message.edit_text("No products available for deletion.")
        return

    await callback.message.edit_text(
        "Select a product to delete:",
        reply_markup=product_list_keyboard_for_deletion(products),
    )


@router.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_product(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        product = await session.get(Product, product_id)
        if product:
            await session.delete(product)
            await session.commit()
            await callback.message.edit_text("Product deleted successfully.")
        else:
            await callback.message.edit_text("Product not found.")
