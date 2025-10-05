from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message
import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.reply(
        '<blockquote><b>Здраствуйте👋!</b> Это бот для организации вашего лучшего путешествия 🛫😎!</blockquote>', 
        parse_mode="HTML"
    )
    await message.answer(
        '⦍🏙️⦎ Пожалуйста, <b>отправьте вашу геолокацию</b>, чтобы я мог определить ваш город.', 
        reply_markup=kb.get_from_location, parse_mode="HTML"
    ) 
