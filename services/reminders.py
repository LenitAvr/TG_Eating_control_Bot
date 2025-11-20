import asyncio
from datetime import datetime
from db.models import AsyncSessionLocal
from db import crud
from zoneinfo import ZoneInfo
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# cache: set of (reminder_id, minute_str)
_sent_cache = set()

async def schedule_loop(bot, interval=30):
    while True:
        now_utc = datetime.utcnow()
        minute_key_utc = now_utc.strftime('%Y-%m-%d %H:%M')
        async with AsyncSessionLocal() as session:
            reminders = await crud.list_active_reminders(session)
            for r in reminders:
                user = r.user
                tz_name = (user.timezone or 'UTC') if user else 'UTC'
                try:
                    local_now = now_utc.replace(tzinfo=ZoneInfo('UTC')).astimezone(ZoneInfo(tz_name))
                except Exception:
                    local_now = now_utc
                hs = local_now.strftime('%H:%M')
                minute_key = local_now.strftime('%Y-%m-%d %H:%M')
                times = (r.times or '').split(',') if r.times else []
                times = [t.strip() for t in times if t.strip()]
                if hs in times:
                    cache_key = (r.id, minute_key)
                    if cache_key in _sent_cache:
                        continue
                    try:
                        kb = InlineKeyboardMarkup()
                        kb.add(InlineKeyboardButton('Добавить приём', callback_data='add_meal'))
                        await bot.send_message(int(r.user.tg_id), f'Напоминание: пора добавить приём пищи (/addmeal) — время по вашему часовому поясу {tz_name}', reply_markup=kb)
                        _sent_cache.add(cache_key)
                    except Exception:
                        pass
        # clear cache entries older than current utc minute across all reminders
        # keep only entries for current utc minute (approximation)
        _sent_cache_copy = set([k for k in _sent_cache if k[1] == minute_key_utc])
        _sent_cache.clear()
        _sent_cache.update(_sent_cache_copy)
        await asyncio.sleep(interval)

# helper wrappers for handlers
async def set_user_reminders_db(tg_id: int, times: list, enabled: bool=True):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg(session, tg_id)
        if not user:
            return None
        r = await crud.set_reminder_for_user(session, user.id, times, enabled)
        return r

async def get_user_reminders_db(tg_id: int):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg(session, tg_id)
        if not user:
            return None
        r = await crud.get_reminder_for_user(session, user.id)
        if not r:
            return {'enabled': False, 'times': []}
        return {'enabled': r.enabled, 'times': (r.times or '').split(',')}

async def delete_user_reminders_db(tg_id: int):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg(session, tg_id)
        if not user:
            return False
        return await crud.delete_reminder_for_user(session, user.id)
