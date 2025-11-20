import asyncio, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./dev.db'
from services import reminders as reminders_svc
from db.models import AsyncSessionLocal
from db import crud
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

class DummyBot:
    def __init__(self, out_file='mock_sends.txt'):
        self.out_file = out_file
    async def send_message(self, tg_id, text, reply_markup=None):
        line = f"SEND to {tg_id}: {text}\n"
        print(line.strip())
        with open(self.out_file, 'a', encoding='utf-8') as f:
            f.write(line)
        return True

async def prepare_reminder(tg_id, tz_name='Europe/Moscow'):
    # compute next minute in user's timezone
    now_utc = datetime.utcnow().replace(tzinfo=ZoneInfo('UTC'))
    try:
        local_now = now_utc.astimezone(ZoneInfo(tz_name))
    except Exception:
        local_now = now_utc
    next_min = (local_now + timedelta(minutes=1)).strftime('%H:%M')
    print('Preparing reminder for', next_min, 'tz', tz_name)
    await reminders_svc.set_user_reminders_db(tg_id, [next_min], enabled=True)

async def main():
    tg = 7027966738
    # ensure admin user exists
    async with AsyncSessionLocal() as session:
        u = await crud.get_user_by_tg(session, tg)
        if not u:
            u = await crud.create_user(session, tg_id=tg, name='Admin', timezone='Europe/Moscow')
            print('created admin user', u.id)
    await prepare_reminder(tg, 'Europe/Moscow')
    bot = DummyBot()
    # run scheduler for ~80 seconds
    task = asyncio.create_task(reminders_svc.schedule_loop(bot, interval=5))
    try:
        await asyncio.sleep(80)
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    print('done')

if __name__ == '__main__':
    asyncio.run(main())

