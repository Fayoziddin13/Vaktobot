from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db import add_employee, add_shift_start, add_shift_end
from datetime import datetime

router = Router()

class RegisterEmployee(StatesGroup):
    full_name = State()
    birth_date = State()
    salary = State()
    phone = State()

@router.callback_query(F.data == "role_employee")
async def register_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Илтимос, тўлиқ исмингизни киритинг:")
    await state.set_state(RegisterEmployee.full_name)

@router.message(RegisterEmployee.full_name)
async def register_birth(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Туғилган сана (YYYY-MM-DD) форматида киритинг:")
    await state.set_state(RegisterEmployee.birth_date)

@router.message(RegisterEmployee.birth_date)
async def register_salary(message: types.Message, state: FSMContext):
    await state.update_data(birth_date=message.text)
    await message.answer("Маошингизни киритинг (сўмда):")
    await state.set_state(RegisterEmployee.salary)

@router.message(RegisterEmployee.salary)
async def register_phone(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await message.answer("Телефон рақамингизни киритинг:")
    await state.set_state(RegisterEmployee.phone)

@router.message(RegisterEmployee.phone)
async def finish_register(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await add_employee(
        user_id=message.from_user.id,
        full_name=data["full_name"],
        birth_date=data["birth_date"],
        salary=data["salary"],
        phone=message.text
    )

    await message.answer(f"Рўйхатдан ўтдингиз, {data['full_name']}. Хуш келибсиз!")

    builder = InlineKeyboardBuilder()
    builder.button(text="Сменани бошлаш",
    callback_data="start_shift")
    builder.button(text="Сменани тугатиш",
    callback_data="end_shaift")
    await message.answer("Илтимос, керакли амални танланг:", reply_markup=builder.as_markup())
    await state.clear()

@router.callback_query(F.data == "start_shift")
async def start_shift(callback: types.CallbackQuery):
    await add_shift_start(callback.from_user.id)
    await callback.message.answer("Смена бошланди. Омад тилаймиз!")

@router.callback_query(F.data == "end_shift")
async def end_shift(callback: types.CallbackQuery):
    await add_shift_end(callback.from_user.id)
    await callback.message.answer("Смена тугади. Рахмат!")