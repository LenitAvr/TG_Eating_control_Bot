from sqlalchemy import select
from sqlalchemy.orm import joinedload
from db.models import User, Product, Meal, MealItem, AsyncSessionLocal, Goal
from typing import Optional
import datetime

async def get_user_by_tg(session, tg_id: int) -> Optional[User]:
    q = await session.execute(select(User).where(User.tg_id==tg_id))
    return q.scalars().first()

async def create_user(session, tg_id: int, name: str = None, **kwargs) -> User:
    user = User(tg_id=tg_id, name=name, **kwargs)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def create_product(session, **data) -> Product:
    prod = Product(**data)
    session.add(prod)
    await session.commit()
    await session.refresh(prod)
    return prod

async def add_meal(session, user_id: str, name: str, timestamp: datetime.datetime, items: list):
    meal = Meal(user_id=user_id, name=name, timestamp=timestamp)
    session.add(meal)
    await session.flush()
    for it in items:
        mi = MealItem(meal_id=meal.id, product_id=it.get('product_id'), custom_name=it.get('custom_name'),
                      weight_g=it['weight_g'], kcal=it['kcal'], protein=it['protein'],
                      fat=it['fat'], carbs=it['carbs'])
        session.add(mi)
    await session.commit()
    await session.refresh(meal)
    return meal

async def search_products(session, qtext: str, limit: int = 20):
    q = await session.execute(select(Product).where(Product.name.ilike(f'%{qtext}%')).limit(limit))
    return q.scalars().all()

# Goal related
async def get_goal_by_user(session, user_id: str) -> Optional[Goal]:
    q = await session.execute(select(Goal).where(Goal.user_id==user_id))
    return q.scalars().first()

async def set_goal(session, user_id: str, kcal: float=None, protein: float=None, fat: float=None, carbs: float=None) -> Goal:
    goal = await get_goal_by_user(session, user_id)
    if not goal:
        goal = Goal(user_id=user_id, kcal=kcal, protein=protein, fat=fat, carbs=carbs)
        session.add(goal)
    else:
        if kcal is not None: goal.kcal = kcal
        if protein is not None: goal.protein = protein
        if fat is not None: goal.fat = fat
        if carbs is not None: goal.carbs = carbs
    await session.commit()
    await session.refresh(goal)
    return goal

async def get_meals_for_user(session, user_id: str, start: datetime.datetime=None, end: datetime.datetime=None):
    q = select(Meal).where(Meal.user_id==user_id)
    if start is not None:
        q = q.where(Meal.timestamp>=start)
    if end is not None:
        q = q.where(Meal.timestamp<end)
    res = await session.execute(q)
    return res.scalars().all()

# Reminders CRUD
async def get_reminder_for_user(session, user_id: str):
    from db.models import Reminder
    q = await session.execute(select(Reminder).where(Reminder.user_id==user_id))
    return q.scalars().first()

async def set_reminder_for_user(session, user_id: str, times: list, enabled: bool=True):
    from db.models import Reminder
    times_str = ','.join(times)
    r = await get_reminder_for_user(session, user_id)
    if not r:
        r = Reminder(user_id=user_id, times=times_str, enabled=enabled)
        session.add(r)
    else:
        r.times = times_str
        r.enabled = enabled
    await session.commit()
    await session.refresh(r)
    return r

async def delete_reminder_for_user(session, user_id: str):
    from db.models import Reminder
    r = await get_reminder_for_user(session, user_id)
    if r:
        await session.delete(r)
        await session.commit()
        return True
    return False

async def list_active_reminders(session):
    from db.models import Reminder
    q = await session.execute(select(Reminder).options(joinedload(Reminder.user)).where(Reminder.enabled==True))
    return q.scalars().all()

# User updates
async def update_user_timezone(session, tg_id: int, timezone: str):
    q = await session.execute(select(User).where(User.tg_id==tg_id))
    user = q.scalars().first()
    if not user:
        return None
    user.timezone = timezone
    await session.commit()
    await session.refresh(user)
    return user
