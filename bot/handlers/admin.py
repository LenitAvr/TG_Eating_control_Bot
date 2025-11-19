from aiogram import Router
from aiogram.types import Message
from core.config import settings
from db.models import AsyncSessionLocal
from db import crud

router = Router()

def is_admin(tg_id: int):
    if not settings.ADMIN_TG_IDS:
        return False
    ids = [int(x.strip()) for x in settings.ADMIN_TG_IDS.split(',') if x.strip()]
    return tg_id in ids

@router.message(commands=['admin_add_product'])
async def admin_add_product(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer('Нет доступа.')
        return
    payload = message.text.partition(' ')[2]
    try:
        name, kcal, protein, fat, carbs, category = [p.strip() for p in payload.split(';')]
    except:
        await message.answer('Формат: /admin_add_product name;kcal;protein;fat;carbs;category')
        return
    async with AsyncSessionLocal() as session:
        prod = await crud.create_product(session,
                                        name=name,
                                        kcal_per_100=float(kcal),
                                        protein_per_100=float(protein),
                                        fat_per_100=float(fat),
                                        carbs_per_100=float(carbs),
                                        category=category)
    await message.answer(f'Добавлен продукт {prod.name} ({prod.kcal_per_100} kcal/100g).')
