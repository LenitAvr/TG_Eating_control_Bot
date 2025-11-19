from aiogram import Router
from aiogram.types import Message
from db.models import AsyncSessionLocal
from db import crud
from services.calories import sum_items
from services.reports import ascii_summary
import datetime

router = Router()

@router.message(commands=['stats'])
async def cmd_stats(message: Message):
    parts = message.text.split()
    period = parts[1] if len(parts) > 1 else 'day'
    now = datetime.datetime.utcnow()
    if period == 'day':
        start = datetime.datetime(now.year, now.month, now.day)
    elif period == 'week':
        start = now - datetime.timedelta(days=now.weekday())
        start = datetime.datetime(start.year, start.month, start.day)
    elif period == 'month':
        start = datetime.datetime(now.year, now.month, 1)
    else:
        await message.answer('Используйте day|week|month')
        return
    end = now + datetime.timedelta(days=1)
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg(session, message.from_user.id)
        if not user:
            await message.answer('Пользователь не найден. /start')
            return
        meals = await session.execute(__import__('sqlalchemy').select(__import__('db').models.Meal).where(__import__('db').models.Meal.user_id==user.id, __import__('db').models.Meal.timestamp>=start, __import__('db').models.Meal.timestamp<end))
        meals = meals.scalars().all()
        items = []
        for m in meals:
            for it in m.items:
                items.append({'kcal': it.kcal, 'protein': it.protein, 'fat': it.fat, 'carbs': it.carbs})
        totals = sum_items(items)
        await message.answer(ascii_summary(totals))
