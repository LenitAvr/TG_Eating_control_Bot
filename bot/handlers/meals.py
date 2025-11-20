from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from db.models import AsyncSessionLocal
from db import crud
from services.calories import calc_item_by_product, sum_items
import datetime

router = Router()

class AddMealStates(StatesGroup):
    NAME = State()
    TIMESTAMP = State()
    ADDING_ITEMS = State()

@router.message(Command("addmeal"))
async def cmd_addmeal(message: Message, state: FSMContext):
    await state.set_state(AddMealStates.NAME)
    await message.answer('Как назвать приём пищи? (пример: Завтрак)')

@router.message(AddMealStates.NAME)
async def meal_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddMealStates.TIMESTAMP)
    await message.answer("Укажите дату/время в формате YYYY-MM-DD HH:MM или 'now'")

@router.message(AddMealStates.TIMESTAMP)
async def meal_time(message: Message, state: FSMContext):
    txt = message.text.strip()
    if txt.lower() == 'now':
        ts = datetime.datetime.utcnow()
    else:
        try:
            ts = datetime.datetime.fromisoformat(txt)
        except:
            await message.answer("Неверный формат. Используйте 'now' или YYYY-MM-DD HH:MM")
            return
    await state.update_data(timestamp=ts.isoformat())
    await state.set_state(AddMealStates.ADDING_ITEMS)
    await message.answer("Добавляйте позиции: '<название или product_id> <вес_в_гр>'. 'done' - закончить.")

@router.message(AddMealStates.ADDING_ITEMS)
async def adding_items(message: Message, state: FSMContext):
    txt = message.text.strip()
    if txt.lower() == 'done':
        data = await state.get_data()
        items = data.get('items', [])
        processed_items = []
        async with AsyncSessionLocal() as session:
            user = await crud.get_user_by_tg(session, message.from_user.id)
            if not user:
                await message.answer('Пользователь не найден, пройдите /start.')
                await state.clear()
                return
            for it in items:
                q = it['q']; weight = it['weight']
                # try product by id
                prod = None
                try:
                    res = await session.execute(__import__('sqlalchemy').select(__import__('db').models.Product).where(__import__('db').models.Product.id==q))
                    prod = res.scalars().first()
                except:
                    prod = None
                if not prod:
                    res = await session.execute(__import__('sqlalchemy').select(__import__('db').models.Product).where(__import__('db').models.Product.name.ilike(f'%{q}%')))
                    prod = res.scalars().first()
                if prod:
                    calc = calc_item_by_product({
                        'kcal_per_100': prod.kcal_per_100,
                        'protein_per_100': prod.protein_per_100,
                        'fat_per_100': prod.fat_per_100,
                        'carbs_per_100': prod.carbs_per_100
                    }, weight)
                    processed_items.append({'product_id': prod.id, 'custom_name': None, 'weight_g': weight, **calc})
                else:
                    calc = calc_item_by_product({'kcal_per_100':0,'protein_per_100':0,'fat_per_100':0,'carbs_per_100':0}, weight)
                    processed_items.append({'product_id': None, 'custom_name': q, 'weight_g': weight, **calc})
            meal = await crud.add_meal(session, user_id=user.id, name=data.get('name'),
                                       timestamp=datetime.datetime.fromisoformat(data.get('timestamp')),
                                       items=processed_items)
        totals = sum_items(processed_items)
        await state.clear()
        await message.answer(f'Приём добавлен. Суммы: {totals}')
        return

    parts = txt.split()
    if len(parts) < 2:
        await message.answer('Формат: <название или product_id> <вес_в_г>')
        return
    q = ' '.join(parts[:-1])
    try:
        weight = float(parts[-1])
    except:
        await message.answer('Неверный вес.')
        return
    data = await state.get_data()
    items = data.get('items', [])
    items.append({'q': q, 'weight': weight})
    await state.update_data(items=items)
    await message.answer(f'Добавлено: {q} — {weight} г. Напишите следующую позицию или done.')
