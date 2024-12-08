from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.models import Product
from database.db_setup import async_session

router = Router()


class CreateProductFSM(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_currency = State()
    waiting_for_seller = State()


@router.callback_query(lambda call: call.data == "create_product")
async def start_create_product(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Enter product name:")
    await state.set_state(CreateProductFSM.waiting_for_name)


@router.message(CreateProductFSM.waiting_for_name)
async def product_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Enter product description:")
    await state.set_state(CreateProductFSM.waiting_for_description)


@router.message(CreateProductFSM.waiting_for_description)
async def product_description_handler(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Enter product price:")
    await state.set_state(CreateProductFSM.waiting_for_price)


@router.message(CreateProductFSM.waiting_for_price)
async def product_price_handler(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await message.answer("Enter product currency (e.g., USD):")
        await state.set_state(CreateProductFSM.waiting_for_currency)
    except ValueError:
        await message.answer("Please enter a valid price.")


@router.message(CreateProductFSM.waiting_for_currency)
async def product_currency_handler(message: types.Message, state: FSMContext):
    await state.update_data(currency=message.text.upper())
    await message.answer("Enter seller's name:")
    await state.set_state(CreateProductFSM.waiting_for_seller)


@router.message(CreateProductFSM.waiting_for_seller)
async def product_seller_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data["seller"] = message.text

    async with async_session() as session:
        new_product = Product(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            currency=data["currency"],
            seller=data["seller"],
        )
        session.add(new_product)
        await session.commit()

    await message.answer(f"Product '{data['name']}' created successfully!")
    await state.clear()
