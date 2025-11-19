from sqlalchemy import select
from db.models import User, Product, Meal, MealItem, Goal, Reminder, AsyncSessionLocal
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
