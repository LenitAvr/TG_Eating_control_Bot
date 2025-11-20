from core.bot_init import dp
from bot.handlers import onboarding, meals, stats, admin, profile, goals, tools, reminders

def register_handlers():
    dp.include_router(onboarding.router)
    dp.include_router(meals.router)
    dp.include_router(stats.router)
    dp.include_router(admin.router)
    dp.include_router(profile.router)
    dp.include_router(goals.router)
    dp.include_router(tools.router)
    dp.include_router(reminders.router)
