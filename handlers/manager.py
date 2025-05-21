from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db import get_all_employees, get_shifts_report

router = Router()

@router.callback_query(lambda c: c.data == "role_manager")
async def manager_panel(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Ходимлар рўйхати", callback_data="employee_list")
    builder.button(text="Сменаларни кўриш", callback_data="shift_list")
    builder.button(text="Ҳисобот", callback_data="report")
    await callback.message.answer("Иш бошқарувчи панели:", reply_markup=builder.as_markup())

@router.callback_query(lambda c: c.data == "employee_list")
async def show_employees(callback: types.CallbackQuery):
    employees = await get_all_employees()
    msg = "\n\n".join([f"{e[1]} | {e[2]} | {e[3]} so'm | {e[4]}" for e in employees])
    await callback.message.answer(f"Ходимлар рўйхати:\n\n{msg}")

@router.callback_query(lambda c: c.data == "report")
async def show_report(callback: types.CallbackQuery):
    report = await get_shifts_report()
    await callback.message.answer(report)