from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

general = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='⦍⛅⦎ Погода')],
                                     [KeyboardButton(text='⦍💸⦎ Местная валюта')],
                                     [KeyboardButton(text='⦍⭐⦎ Интересные места')]],
                        resize_keyboard=True,
                        input_field_placeholder='Что вас интересует...')

get_from_location = ReplyKeyboardMarkup(keyboard=[
                                    [KeyboardButton(text="⦍🌐⦎ Отправить геолокацию", request_location=True)],
                                    [KeyboardButton(text="⦍✍️⦎ Ввести город вручную")]],
                        resize_keyboard=True,
                        one_time_keyboard=True
) 
check_location = InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton(text='Да', callback_data="location_yes")],
                                     [InlineKeyboardButton(text='Нет', callback_data="location_no")]]
                        )
check_location_to = InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton(text='Да', callback_data="city_yes")],
                                     [InlineKeyboardButton(text='Нет', callback_data="city_no")]]
                        )

check_location_from = InlineKeyboardMarkup(inline_keyboard=[
                                     [InlineKeyboardButton(text='Да', callback_data="city_from_yes")],
                                     [InlineKeyboardButton(text='Нет', callback_data="city_from_no")]]
                        )