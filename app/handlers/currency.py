from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import app.functions as fc

router = Router()

@router.message(F.text == '⦍💸⦎ Местная валюта')    
async def get_city_currency(message: Message, state: FSMContext):
    data = await state.get_data()
    city_to = data.get("city_to")

    coord = await fc.get_weather(city_to)
    country_code = await fc.get_attractions(city_to, coord['lat'], coord['lon'])

    if not country_code:
        await message.answer("⦍⚠️⦎ Не удалось определить страну назначения.")
        return

    code_country = country_code[0]['country_code']
    currency = await fc.get_currency(code_country)
    conv = await fc.convert_currency(currency)

    text = (
        f"⦍💱⦎ <b>Курс валюты</b>:\n"
        f'⟥─────────────⟤\n'
        f"⦍💰⦎ <b>1</b> {conv['base_code']} = <b>{conv['conversion_result']}</b> RUB\n"
    )
    await message.answer(text, parse_mode="HTML")
