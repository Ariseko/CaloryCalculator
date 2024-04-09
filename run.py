import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from app.handlers import router

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main(dp):
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main(dp))
    except KeyboardInterrupt:
        print('Exit')
