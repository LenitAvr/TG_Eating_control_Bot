import asyncio, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./dev.db'
from services.reminders import set_user_reminders_db, get_user_reminders_db

async def main():
    tg_id = 7027966738
    r = await set_user_reminders_db(tg_id, ['08:00','12:00','19:00'], enabled=True)
    print('set:', r.id if r else None)
    cfg = await get_user_reminders_db(tg_id)
    print('cfg:', cfg)

if __name__ == '__main__':
    asyncio.run(main())

