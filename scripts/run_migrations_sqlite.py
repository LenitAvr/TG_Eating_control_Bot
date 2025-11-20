import os
from alembic.config import Config
from alembic import command

# Устанавливаем переменную окружения для этого процесса (локальная sqlite)
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./dev.db'

cfg = Config('alembic.ini')
print('Running alembic upgrade head using DATABASE_URL=', os.environ['DATABASE_URL'])
command.upgrade(cfg, 'head')
print('Migrations applied')

