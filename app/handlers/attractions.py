from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import app.functions as fc

router = Router()

@router.message(F.text == '⦍⭐⦎ Интересные места')
async def interesting_places(message: Message, state: FSMContext):
    data = await state.get_data()
    city_to = data.get("city_to")
    coord = await fc.get_weather(city_to)

    try:
        attractions = await fc.get_attractions(city_to, coord['lat'], coord['lon'])
    except Exception as e:
        await message.answer(f"⦍⚠️⦎ Не удалось получить данные: {e}")
        return

    if not attractions:
        await message.answer(f"⦍😕⦎ Не удалось найти достопримечательностей в городе {city_to}.")
        return

    text = f"⦍⭐⦎ Вот что можно посмотреть в <b>{city_to}</b>:\n\n"
    for attraction in attractions:
        text += f"⦍📍⦎ <b>{attraction['name'].capitalize()}</b>\n{attraction['address'].capitalize()}\n\n"

    await message.answer(text, parse_mode="HTML")
