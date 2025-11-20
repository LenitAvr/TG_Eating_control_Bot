import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine
from db.models import Base
from core.config import settings

# Для локальной разработки используем sqlite; переопределяем URL
DATABASE_URL = 'sqlite:///./dev.db'

print('Creating tables using', DATABASE_URL)
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
print('Tables created')
