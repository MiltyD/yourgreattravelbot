from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.handlers.city_from import States
import app.keyboards as kb
import app.functions as fc

router = Router()

@router.message(States.waiting_city_to)
async def city_to_check (message: Message, state: FSMContext):
    city_to = message.text
    city_true = await fc.get_city_suggestion(city_to)

    await state.update_data(city_to=city_to, city_true=city_true)

    if city_true == "none":
        code_to = await fc.get_city_code(city_to)
        await state.update_data(code_to=code_to)
        await message.answer("⦍🕑⦎ Введите <b>дату вылета</b>", parse_mode="HTML")
        await state.set_state(States.waiting_date)
    else:
        await message.answer(
            f"⦍💡⦎ Возможно, вы имели в виду <b>{city_true}</b>?", 
            reply_markup=kb.check_location_to, 
            parse_mode="HTML"
        )

@router.callback_query(F.data == "city_yes")
async def city_to_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    city_to = data.get("city_true")
    code_to = await fc.get_city_code(city_to)
    await state.update_data(city_to=city_to, code_to=code_to)
    await callback.message.answer("⦍🕑⦎ Введите <b>дату вылета</b>", parse_mode="HTML")
    await state.set_state(States.waiting_date)

@router.callback_query((F.data == "location_yes") | (F.data == "city_no"))
async def city_to_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("⦍🧳⦎ Введите <b>город прибытия</b>", parse_mode="HTML")
    await state.set_state(States.waiting_city_to)
