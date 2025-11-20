import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from core.config import settings
from services.reminders import schedule_loop

# Создаём экземпляр бота
bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(parse_mode="HTML")
)

# Создаём диспетчер с памятью для FSM
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Тестовый пример обработчика (только для команды /hello)
@dp.message(Command("hello"))
async def hello_handler(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

# Функция запуска бота
async def main():
    try:
        print("Бот стартует...")
        # Запускаем планировщик напоминаний в фоне
        asyncio.create_task(schedule_loop(bot))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
