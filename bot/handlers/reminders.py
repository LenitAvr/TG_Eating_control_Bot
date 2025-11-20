from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F
from db.models import AsyncSessionLocal
from db import crud
from services import reminders as reminders_svc
from bot.handlers.meals import AddMealStates

router = Router()

class RemindStates(StatesGroup):
    TIMES = State()

@router.message(Command('reminders'))
async def cmd_reminders(message: Message, state: FSMContext):
    cfg = await reminders_svc.get_user_reminders_db(message.from_user.id)
    if cfg is None:
        await message.answer('Пользователь не найден. Используйте /start')
        return
    if cfg.get('enabled'):
        await message.answer(f"Напоминания включены. Времена: {', '.join(cfg.get('times', []))}\nЧтобы выключить, отправьте 'off'. Чтобы изменить — пришлите новые времена в формате HH:MM, через запятую.")
    else:
        await message.answer("Напоминания выключены. Чтобы включить, пришлите времена в формате HH:MM через запятую, например: 08:00,13:00,19:00")
    await state.set_state(RemindStates.TIMES)

@router.message(RemindStates.TIMES)
async def set_times(message: Message, state: FSMContext):
    txt = message.text.strip().lower()
    if txt == 'off':
        ok = await reminders_svc.delete_user_reminders_db(message.from_user.id)
        await state.clear()
        await message.answer('Напоминания отключены.' if ok else 'Напоминания не найдены.')
        return
    # parse times
    parts = [p.strip() for p in message.text.split(',') if p.strip()]
    valid = []
    for p in parts:
        try:
            h, m = p.split(':')
            hh = int(h); mm = int(m)
            if 0 <= hh < 24 and 0 <= mm < 60:
                valid.append(f"{hh:02d}:{mm:02d}")
        except Exception:
            pass
    if not valid:
        await message.answer('Неверный формат. Пример: 08:00,13:00,19:00 или отправьте off для отключения.')
        return
    r = await reminders_svc.set_user_reminders_db(message.from_user.id, valid, enabled=True)
    await state.clear()
    if r:
        await message.answer(f'Напоминания установлены: {", ".join(valid)}')
    else:
        await message.answer('Не удалось установить напоминания (пользователь не найден).')

@router.callback_query(F.data == 'add_meal')
async def on_add_meal_callback(query: CallbackQuery, state: FSMContext):
    await state.set_state(AddMealStates.NAME)
    await query.answer()
    await query.message.answer('Как назвать приём пищи? (пример: Завтрак)')
