import asyncio, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./dev.db'
from db.models import AsyncSessionLocal
from db import crud
from services.reminders import set_user_reminders_db
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

async def main(tg_id:int, tz_name='Europe/Moscow'):
    # compute next minute in user's timezone
    now_utc = datetime.utcnow().replace(tzinfo=ZoneInfo('UTC'))
    try:
        local_now = now_utc.astimezone(ZoneInfo(tz_name))
    except Exception:
        local_now = now_utc
    next_min = (local_now + timedelta(minutes=1)).strftime('%H:%M')
    print('Setting reminder for', next_min, 'in timezone', tz_name)
    r = await set_user_reminders_db(tg_id, [next_min], enabled=True)
    print('Result id', getattr(r, 'id', None))

if __name__ == '__main__':
    asyncio.run(main(7027966738, 'Europe/Moscow'))

