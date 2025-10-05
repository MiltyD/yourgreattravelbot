from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb
import app.functions as fc

router = Router()

class States(StatesGroup):
    waiting_city_from = State()
    waiting_city_to = State()
    waiting_date = State()

@router.message(F.location)
async def get_city_from_location(message: Message, state: FSMContext):
    lat = message.location.latitude + 0.1
    lng = message.location.longitude - 0.1
    city_from = await fc.get_city(lat, lng)
    code_from = await fc.get_city_code(city_from)

    await state.update_data(city_from=city_from, code_from=code_from, lat=lat, lng=lng)

    await message.answer(
        f"⦍🤔⦎ Ваш город — <b>{city_from}</b>?", 
        reply_markup=kb.check_location, 
        parse_mode="HTML"
    )

@router.message(F.text == "⦍✍️⦎ Ввести город вручную")
async def input_city_from(message: Message, state: FSMContext):
    await message.answer("⦍🧳⦎ Введите <b>город отправления</b>", parse_mode="HTML")
    await state.set_state(States.waiting_city_from) 

@router.callback_query((F.data == "location_no") | (F.data == "city_from_no"))
async def city_from_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("⦍🧳⦎ Введите <b>город отправления</b>", parse_mode="HTML")
    await state.set_state(States.waiting_city_from)

@router.message(States.waiting_city_from)
async def city_from_check(message: Message, state: FSMContext):
    city_from = message.text
    city_true_from = await fc.get_city_suggestion(city_from)

    await state.update_data(city_from=city_from, city_true_from=city_true_from)

    if city_true_from == "none":
        code_from = await fc.get_city_code(city_from)
        await state.update_data(city_from=city_from, code_from=code_from)
        await message.answer("⦍🧳⦎ Введите <b>город прибытия</b>", parse_mode="HTML")
        await state.set_state(States.waiting_city_to)
    else:
        await message.answer(
            f"⦍💡⦎ Возможно, вы имели в виду <b>{city_true_from}</b>?", 
            reply_markup=kb.check_location_from, 
            parse_mode="HTML"
        )

@router.callback_query(F.data == "city_from_yes")
async def city_from_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    city_from = data.get("city_true_from")
    code_from = await fc.get_city_code(city_from)
    await state.update_data(city_from=city_from, code_from=code_from)
    await callback.message.answer("⦍🧳⦎ Введите <b>город прибытия</b>", parse_mode="HTML")
    await state.set_state(States.waiting_city_to)
