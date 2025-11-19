import asyncio
from core.bot_init import dp, bot
from bot import __init__ as bot_init

if __name__ == '__main__':
    bot_init.register_handlers()
    print('Starting FoodDiary bot...')
    asyncio.run(dp.start_polling(bot))
