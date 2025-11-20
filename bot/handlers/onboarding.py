from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from db.models import AsyncSessionLocal
from db import crud
from bot.messages import *

router = Router()

class OnboardStates(StatesGroup):
    NAME = State()
    WEIGHT = State()
    HEIGHT = State()
    AGE = State()
    ACTIVITY = State()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg(session, message.from_user.id)
        if user:
            await message.answer('С возвращением! Используйте /help.')
            return
    await state.set_state(OnboardStates.NAME)
    await message.answer(WELCOME)

@router.message(OnboardStates.NAME)
async def name_step(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OnboardStates.WEIGHT)
    await message.answer(ASK_WEIGHT)

@router.message(OnboardStates.WEIGHT)
async def weight_step(message: Message, state: FSMContext):
    try:
        w = float(message.text)
    except:
        await message.answer('Неверный формат. Введите число, например 72.5')
        return
    await state.update_data(weight=w)
    await state.set_state(OnboardStates.HEIGHT)
    await message.answer(ASK_HEIGHT)

@router.message(OnboardStates.HEIGHT)
async def height_step(message: Message, state: FSMContext):
    try:
        h = float(message.text)
    except:
        await message.answer('Неверный формат. Введите число в см, например 175')
        return
    await state.update_data(height=h)
    await state.set_state(OnboardStates.AGE)
    await message.answer(ASK_AGE)

@router.message(OnboardStates.AGE)
async def age_step(message: Message, state: FSMContext):
    try:
        a = int(message.text)
    except:
        await message.answer('Неверный формат. Введите целое число, например 30')
        return
    await state.update_data(age=a)
    await state.set_state(OnboardStates.ACTIVITY)
    await message.answer(ASK_ACTIVITY)

@router.message(OnboardStates.ACTIVITY)
async def activity_step(message: Message, state: FSMContext):
    data = await state.get_data()
    activity = message.text
    async with AsyncSessionLocal() as session:
        user = await crud.create_user(session, tg_id=message.from_user.id, name=data.get('name'),
                                      weight=data.get('weight'), height=data.get('height'),
                                      age=data.get('age'), activity_level=activity)
    await state.clear()
    await message.answer(PROFILE_UPDATED)
