import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties
from core.config import settings

# Создаём экземпляр бота
bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(parse_mode="HTML")
)

# Создаём диспетчер
dp = Dispatcher()

# Пример простого хэндлера
@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

# Функция запуска бота
async def main():
    try:
        print("Бот стартует...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
