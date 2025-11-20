from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from db.models import AsyncSessionLocal
from db import crud

router = Router()

class GoalStates(StatesGroup):
    KCAL = State()
    PROTEIN = State()
    FAT = State()
    CARBS = State()

@router.message(Command('setgoal'))
async def cmd_setgoal(message: Message, state: FSMContext):
    await state.set_state(GoalStates.KCAL)
    await message.answer('Укажите дневную цель по калориям (kcal), например 2000:')

@router.message(GoalStates.KCAL)
async def set_kcal(message: Message, state: FSMContext):
    try:
        kcal = float(message.text)
    except:
        await message.answer('Неверный формат. Введите число, например 2000')
        return
    await state.update_data(kcal=kcal)
    await state.set_state(GoalStates.PROTEIN)
    await message.answer('Укажите белки (г):')

@router.message(GoalStates.PROTEIN)
async def set_protein(message: Message, state: FSMContext):
    try:
        protein = float(message.text)
    except:
        await message.answer('Неверный формат. Введите число')
        return
    await state.update_data(protein=protein)
    await state.set_state(GoalStates.FAT)
    await message.answer('Укажите жиры (г):')

@router.message(GoalStates.FAT)
async def set_fat(message: Message, state: FSMContext):
    try:
        fat = float(message.text)
    except:
        await message.answer('Неверный формат. Введите число')
        return
    await state.update_data(fat=fat)
    await state.set_state(GoalStates.CARBS)
    await message.answer('Укажите углеводы (г):')

@router.message(GoalStates.CARBS)
async def set_carbs(message: Message, state: FSMContext):
    try:
        carbs = float(message.text)
    except:
        await message.answer('Неверный формат. Введите число')
        return
    data = await state.get_data()
    data['carbs'] = carbs
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg(session, message.from_user.id)
        if not user:
            await message.answer('Пользователь не найден. Используйте /start')
            await state.clear()
            return
        goal = await crud.set_goal(session, user.id, kcal=data.get('kcal'), protein=data.get('protein'), fat=data.get('fat'), carbs=data.get('carbs'))
    await state.clear()
    await message.answer(f'Цель установлена: {goal.kcal} kcal, P:{goal.protein}g F:{goal.fat}g C:{goal.carbs}g')

