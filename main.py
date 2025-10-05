import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import routers


async def main():
    bot = Bot(token='7926924892:AAETtpREx1v18QXyVxGTbbm5igH3LeDWnWM')
    dp = Dispatcher()
    for r in routers: dp.include_router(r)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')