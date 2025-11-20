from core.bot_init import main
import bot as bot_pkg

if __name__ == '__main__':
    bot_pkg.register_handlers()
    print('Starting FoodDiary bot...')
    import asyncio
    asyncio.run(main())
