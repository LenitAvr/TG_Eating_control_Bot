from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from db.models import AsyncSessionLocal
from db import crud
from zoneinfo import ZoneInfo, available_timezones

router = Router()

@router.message(Command('profile'))
async def cmd_profile(message: Message):
    async with AsyncSessionLocal() as session:
        user = await crud.get_user_by_tg(session, message.from_user.id)
        if not user:
            await message.answer('Профиль не найден. Используйте /start для регистрации.')
            return
        text = f"Имя: {user.name or '—'}\nВес: {user.weight or '—'} кг\nРост: {user.height or '—'} см\nВозраст: {user.age or '—'}\nАктивность: {user.activity_level or '—'}\nTimezone: {user.timezone or 'UTC'}"
        await message.answer(text)

class TZStates(StatesGroup):
    INPUT = State()

@router.message(Command('settimezone'))
async def cmd_settimezone(message: Message, state: FSMContext):
    await state.set_state(TZStates.INPUT)
    await message.answer('Укажите вашу временную зону (IANA), например Europe/Moscow или UTC. Отправьте "list" чтобы получить несколько популярных вариантов.')

@router.message(TZStates.INPUT)
async def set_timezone_state(message: Message, state: FSMContext):
    txt = message.text.strip()
    if txt.lower() == 'list':
        samples = ['UTC','Europe/Moscow','Europe/London','America/New_York','Asia/Tokyo']
        await message.answer('Примеры: ' + ', '.join(samples))
        return
    try:
        tz = ZoneInfo(txt)
    except Exception:
        await message.answer('Не удалось распознать timezone. Убедитесь, что используете IANA имя, например Europe/Moscow')
        return
    async with AsyncSessionLocal() as session:
        user = await crud.update_user_timezone(session, message.from_user.id, txt)
        if not user:
            await message.answer('Пользователь не найден. Используйте /start')
            await state.clear()
            return
    await state.clear()
    await message.answer(f'Timezone обновлён: {txt}')

@router.message(Command('help'))
async def cmd_help(message: Message):
    from bot.messages import HELP
    await message.answer(HELP)
