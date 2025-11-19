from core.bot_init import dp
from bot.handlers import onboarding, meals, stats, admin

def register_handlers():
    dp.include_router(onboarding.router)
    dp.include_router(meals.router)
    dp.include_router(stats.router)
    dp.include_router(admin.router)
