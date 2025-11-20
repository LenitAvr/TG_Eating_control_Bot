import asyncio, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./dev.db'
from db.models import AsyncSessionLocal
from db import crud

async def main(tg_id:int, name:str='Admin', tz: str=None):
    async with AsyncSessionLocal() as session:
        u = await crud.get_user_by_tg(session, tg_id)
        if u:
            print('Exists:', u.id)
            return
        u = await crud.create_user(session, tg_id=tg_id, name=name, timezone=tz)
        print('Created user id=', u.id)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python scripts/create_admin_with_tz.py <tg_id> [tz]')
    else:
        tg = int(sys.argv[1])
        tz = sys.argv[2] if len(sys.argv) > 2 else None
        asyncio.run(main(tg, 'Admin', tz))

