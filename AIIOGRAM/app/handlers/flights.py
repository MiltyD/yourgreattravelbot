from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.handlers.city_from import States
import datetime
from dateutil.parser import parse
import app.functions as fc
import app.keyboards as kb

router = Router()

@router.message(States.waiting_date)
async def departure_date(message: Message, state: FSMContext):
    data = await state.get_data()
    city_from = data.get("city_from")
    code_from = data.get("code_from")
    city_to = data.get("city_to")
    code_to = data.get("code_to")

    date_input = message.text.lower()
    month_ru = {
        'января': 'January', 'январь': 'January',
        'февраля': 'February', 'февраль': 'February',
        'марта': 'March', 'март': 'March',
        'апреля': 'April', 'апрель': 'April',
        'мая': 'May', 'май': 'May',
        'июня': 'June', 'июнь': 'June',
        'июля': 'July', 'июль': 'July',
        'августа': 'August', 'август': 'August',
        'сентября': 'September', 'сентябрь': 'September',
        'октября': 'October', 'октябрь': 'October',
        'ноября': 'November', 'ноябрь': 'November',
        'декабря': 'December', 'декабрь': 'December'
    }

    try:
        for rus_month, eng_month in month_ru.items():
            if rus_month in date_input:
                date_input = date_input.replace(rus_month, eng_month)
                break

        parsed_date = parse(
            date_input,
            dayfirst=True,
            yearfirst=False,
            default=datetime.datetime.now()
        )

        if parsed_date.year == datetime.datetime.now().year and parsed_date.date() < datetime.date.today():
            parsed_date = parsed_date.replace(year=2025)

        date_obj = parsed_date.date()
        date_input = date_obj.strftime('%Y-%m-%d')

    except ValueError:
        await message.answer("⦍⛔⦎ Неверный формат даты. Введите дату, например 5 июня.")
        return
    
    flights = await fc.get_flights(code_from, code_to, date_input)
    date_input = date_obj.strftime('%d.%m.%Y')
    
    if not flights:
        await message.answer(
            f"⦍😕⦎ Рейсы по маршруту <b>{city_from}</b> - <b>{city_to}</b> на <b>{date_input}</b> не найдены.", 
            parse_mode="HTML"
        )
        return
    
    await message.answer(
        f"⦍🗓️⦎ Доступные рейсы <b>{city_from}</b> - <b>{city_to}</b> на <b>{date_input}</b>:",
        parse_mode="HTML"
    )
    
    for flight in flights:
        departure = datetime.datetime.fromisoformat(flight["departure"]).strftime("%H:%M")
        arrival = datetime.datetime.fromisoformat(flight["arrival"]).strftime("%H:%M")
        icon = "🚂" if flight["transport_type"] == "train" else "🛫"

        text = (
            f'⦍{icon}⦎ Рейс "<b>{flight["title"]}</b>" ⦍<b>{flight["number"]}</b>⦎\n'
            f'⟥─────────────⟤\n'
            f'⦍🗓️⦎ Отправление: <b>{flight["fromm"]}</b> <blockquote>{departure}</blockquote>\n'
            f'⦍🕐⦎ Время в пути: <b>{int(flight["duration"])//86400} дней {int(flight["duration"])%86400//3600} часов</b>\n'
            f'⦍🏁⦎ Прибытие: <b>{flight["to"]}</b> <blockquote>{arrival}</blockquote>\n'
        )

        await message.answer(text, parse_mode="HTML")

    await message.answer(
        "<blockquote><b> ⦍🤩⦎ Теперь вы можете получить необходимую информацию для вашего путешествия </b></blockquote>", 
        reply_markup=kb.general, parse_mode="HTML"
    )
    await state.set_state(None)
