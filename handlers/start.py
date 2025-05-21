from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Танлаш", callback_data="choose_role")
    await message.answer(
        "Ассалому алайкум! Vakto ботга хуш келибсиз. Илтимос, ўзингизга тегишли ролни танланг.",
        reply_markup=builder.as_markup()
    )

@router.callback_query(lambda c: c.data == "choose_role")
async def show_roles(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Менежер", callback_data="role_manager")
    builder.button(text="Ходим", callback_data="role_employee")
    await callback.message.edit_text(
        "Аъло! Илтимос, ўз ролингизни танланг:",
        reply_markup=builder.as_markup()
    )