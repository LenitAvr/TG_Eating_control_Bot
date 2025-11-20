from aiogram import Router
from aiogram.types import Message, InputFile
from aiogram.filters import Command
from db.models import AsyncSessionLocal
from db import crud
from services.reports import build_csv_meals
import datetime

router = Router()

@router.message(Command('export'))
async def cmd_export(message: Message):
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
        meals = await crud.get_meals_for_user(session, user.id, start=start, end=end)
        serial = []
        for m in meals:
            serial.append({'timestamp': m.timestamp.isoformat(), 'name': m.name, 'items': [{'custom_name': it.custom_name,'weight_g': it.weight_g,'kcal': it.kcal,'protein': it.protein,'fat': it.fat,'carbs': it.carbs} for it in m.items]})
        csv_bytes = build_csv_meals(serial)
        await message.answer_document(InputFile(io_bytes:=csv_bytes, filename=f'meals_{period}.csv'))

@router.message(Command('searchfood'))
async def cmd_searchfood(message: Message):
    q = message.text.partition(' ')[2].strip()
    if not q:
        await message.answer('Используйте: /searchfood <query>')
        return
    async with AsyncSessionLocal() as session:
        prods = await crud.search_products(session, q)
        if not prods:
            await message.answer('Продукты не найдены')
            return
        lines = []
        for p in prods[:10]:
            lines.append(f'{p.name} — {p.kcal_per_100} kcal/100g (id: {p.id})')
        await message.answer('\n'.join(lines))

