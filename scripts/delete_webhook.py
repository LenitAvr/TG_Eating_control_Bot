import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.config import settings
from aiogram import Bot
import asyncio

async def main():
    bot = Bot(token=settings.bot_token)
    try:
        ok = await bot.delete_webhook(drop_pending_updates=True)
        print('delete_webhook result:', ok)
    except Exception as e:
        print('error deleting webhook:', repr(e))
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())

