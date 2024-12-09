from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.future import select

from database.db_setup import async_session
from database.models import Product
from bot.keyboards.product import product_list_keyboard_for_updating


router = Router()


class UpdateProductState(StatesGroup):
    waiting_for_product_data = State()


@router.callback_query(lambda c: c.data == "update_product")
async def list_products_for_update(callback: CallbackQuery) -> None:
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

    if not products:
        await callback.message.edit_text("No products available for update.")
        return

    await callback.message.edit_text(
        "Select a product to update:",
        reply_markup=product_list_keyboard_for_updating(products),
    )


@router.callback_query(lambda c: c.data.startswith("update_"))
async def prompt_update_product(callback: CallbackQuery, state: FSMContext) -> None:
    product_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        product = await session.get(Product, product_id)

    if not product:
        await callback.message.edit_text("Product not found.")
        return

    await state.update_data(product_id=product_id)

    await callback.message.edit_text(
        f"Editing Product: {product.name}\n\nSend a message in the format:\n"
        f"`name|description|price|currency|seller`"
    )

    await state.set_state(UpdateProductState.waiting_for_product_data)


@router.message(UpdateProductState.waiting_for_product_data)
async def update_product_in_db(message: Message, state: FSMContext) -> None:
    user_input = message.text

    try:
        name, description, price, currency, seller = user_input.split("|")
        price = float(price)
    except ValueError:
        await message.reply(
            "Invalid format. Please use the format:\n"
            "`name|description|price|currency|seller`"
        )
        return

    state_data = await state.get_data()
    product_id = state_data.get("product_id")

    if not product_id:
        await message.reply("Error: Product ID is missing.")
        return

    async with async_session() as session:
        product = await session.get(Product, product_id)
        if not product:
            await message.reply("Product not found.")
            return

        product.name = name.strip()
        product.description = description.strip()
        product.price = price
        product.currency = currency.strip()
        product.seller = seller.strip()

        await session.commit()
        await message.reply(f"Product {product.name} updated successfully!")

    await state.clear()
