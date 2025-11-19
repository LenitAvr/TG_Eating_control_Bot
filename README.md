# FoodDiary — Telegram Bot (Food Diary & Nutrition)

**Tech stack**: Python 3.10+, Aiogram v3, SQLAlchemy (async), Alembic, PostgreSQL (production), SQLite (dev), Pydantic.

## Что реализовано
- Регистрация через `/start` и пошаговое заполнение профиля.
- Добавление приёма пищи вручную; поиск продуктов по базе.
- Подсчёт калорий и БЖУ (per 100g → per portion).
- Установка целей (дневных) и просмотр статистики `/stats day|week|month`.
- Экспорт CSV (services/reports.build_csv_meals).
- Отдельный админ-командный набор (`/admin_add_product`) — доступ по ADMIN_TG_IDS.
- Минимальные unit-tests.

## Структура
(см. дерево в корне)

## Быстрый старт (локально)
1. Скопируйте проект.
2. Создайте `.env` (пример ниже).
3. Установите зависимости:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
