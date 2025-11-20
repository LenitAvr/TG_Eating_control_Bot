import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from core.config import settings
import datetime, uuid

DATABASE_URL = settings.database_url
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

def now():
    return datetime.datetime.utcnow()

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.String, primary_key=True, default=gen_uuid)
    tg_id = sa.Column(sa.BigInteger, unique=True, index=True, nullable=False)
    name = sa.Column(sa.String, nullable=True)
    weight = sa.Column(sa.Float, nullable=True)
    height = sa.Column(sa.Float, nullable=True)
    age = sa.Column(sa.Integer, nullable=True)
    gender = sa.Column(sa.String, nullable=True)
    activity_level = sa.Column(sa.String, nullable=True)
    theme = sa.Column(sa.String, nullable=True)
    avatar = sa.Column(sa.String, nullable=True)
    timezone = sa.Column(sa.String, nullable=True)  # IANA timezone name, e.g. Europe/Moscow
    created_at = sa.Column(sa.DateTime, default=now)
    updated_at = sa.Column(sa.DateTime, default=now, onupdate=now)

    meals = relationship('Meal', back_populates='user')
    goals = relationship('Goal', back_populates='user', uselist=False)
    reminders = relationship('Reminder', back_populates='user', cascade='all, delete-orphan')

class Product(Base):
    __tablename__ = 'products'
    id = sa.Column(sa.String, primary_key=True, default=gen_uuid)
    name = sa.Column(sa.String, index=True, nullable=False)
    brand = sa.Column(sa.String, nullable=True)
    kcal_per_100 = sa.Column(sa.Float, nullable=False)
    protein_per_100 = sa.Column(sa.Float, nullable=False, default=0)
    fat_per_100 = sa.Column(sa.Float, nullable=False, default=0)
    carbs_per_100 = sa.Column(sa.Float, nullable=False, default=0)
    category = sa.Column(sa.String, nullable=True)
    created_by = sa.Column(sa.String, nullable=True)
    created_at = sa.Column(sa.DateTime, default=now)

class Meal(Base):
    __tablename__ = 'meals'
    id = sa.Column(sa.String, primary_key=True, default=gen_uuid)
    user_id = sa.Column(sa.String, sa.ForeignKey('users.id'), nullable=False, index=True)
    name = sa.Column(sa.String, nullable=True)
    timestamp = sa.Column(sa.DateTime, default=now, index=True)
    created_at = sa.Column(sa.DateTime, default=now)

    user = relationship('User', back_populates='meals')
    items = relationship('MealItem', back_populates='meal', cascade='all, delete-orphan')

class MealItem(Base):
    __tablename__ = 'meal_items'
    id = sa.Column(sa.String, primary_key=True, default=gen_uuid)
    meal_id = sa.Column(sa.String, sa.ForeignKey('meals.id'), nullable=False, index=True)
    product_id = sa.Column(sa.String, sa.ForeignKey('products.id'), nullable=True)
    custom_name = sa.Column(sa.String, nullable=True)
    weight_g = sa.Column(sa.Float, nullable=False)
    kcal = sa.Column(sa.Float, nullable=False)
    protein = sa.Column(sa.Float, nullable=False)
    fat = sa.Column(sa.Float, nullable=False)
    carbs = sa.Column(sa.Float, nullable=False)

    meal = relationship('Meal', back_populates='items')
    product = relationship('Product')

class Goal(Base):
    __tablename__ = 'goals'
    id = sa.Column(sa.String, primary_key=True, default=gen_uuid)
    user_id = sa.Column(sa.String, sa.ForeignKey('users.id'), nullable=False, unique=True)
    kcal = sa.Column(sa.Float, nullable=True)
    protein = sa.Column(sa.Float, nullable=True)
    fat = sa.Column(sa.Float, nullable=True)
    carbs = sa.Column(sa.Float, nullable=True)
    updated_at = sa.Column(sa.DateTime, default=now, onupdate=now)

    user = relationship('User', back_populates='goals')

class Reminder(Base):
    __tablename__ = 'reminders'
    id = sa.Column(sa.String, primary_key=True, default=gen_uuid)
    user_id = sa.Column(sa.String, sa.ForeignKey('users.id'), nullable=False, index=True)
    times = sa.Column(sa.String, nullable=True)  # comma-separated HH:MM
    enabled = sa.Column(sa.Boolean, default=True)
    created_at = sa.Column(sa.DateTime, default=now)
    updated_at = sa.Column(sa.DateTime, default=now, onupdate=now)

    user = relationship('User', back_populates='reminders')
