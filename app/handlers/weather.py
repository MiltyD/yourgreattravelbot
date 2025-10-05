from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import app.functions as fc

router = Router()

@router.message(F.text == '⦍⛅⦎ Погода')
async def get_city_weather(message: Message, state: FSMContext):
    data = await state.get_data()
    city_from = data.get("city_from")
    city_to = data.get("city_to")
    
    icon_map = {
        "01d": "☀️", "01n": "🌙",
        "02d": "🌤️", "02n": "🌤️",
        "03d": "☁️", "03n": "☁️",
        "04d": "☁️", "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️",
        "10d": "🌦️", "10n": "🌦️",
        "11d": "⛈️", "11n": "⛈️",
        "13d": "❄️", "13n": "❄️",
        "50d": "🌫️", "50n": "🌫️",
    }
    
    weather_from = await fc.get_weather(city_from)
    weather_to = await fc.get_weather(city_to)
    
    emoji1 = icon_map.get(weather_from["icon"], "❔")
    emoji2 = icon_map.get(weather_to["icon"], "❔")

    text1 = (
        f"⦍📝⦎ <b>Погода в {city_from}</b>:\n"
        f'⟥─────────────⟤\n'
        f"⦍🌡️⦎ Температура: <b>{int(weather_from['temp'])}°C</b> (ощущается как <b>{int(weather_from['feels_like'])}°C</b>)\n"
        f"⦍{emoji1}⦎ {weather_from['description'].capitalize()}"
    )

    text2 = (
        f"⦍📝⦎ <b>Погода в {city_to}</b>:\n"
        f'⟥─────────────⟤\n'
        f"⦍🌡️⦎ Температура: <b>{int(weather_to['temp'])}°C</b> (ощущается как <b>{int(weather_to['feels_like'])}°C</b>)\n"
        f"⦍{emoji2}⦎ {weather_to['description'].capitalize()}"
    )
        
    await message.answer(text1, parse_mode="HTML")
    await message.answer(text2, parse_mode="HTML")
