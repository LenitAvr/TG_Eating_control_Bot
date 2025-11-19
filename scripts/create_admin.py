import asyncio
from db.models import AsyncSessionLocal
from db import crud

async def main(tg_id:int, name:str='Admin'):
    async with AsyncSessionLocal() as session:
        u = await crud.get_user_by_tg(session, tg_id)
        if u:
            print('Exists:', u.id); return
        u = await crud.create_user(session, tg_id=tg_id, name=name)
        print('Created user id=', u.id)
        print('Add tg_id to ADMIN_TG_IDS in .env')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python scripts/create_admin.py <tg_id>')
    else:
        asyncio.run(main(int(sys.argv[1])))
