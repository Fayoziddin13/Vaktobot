import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db import init_db

# Ҳар бир handler'ларни импорт қилиш
from handlers.start import router as start_router
from handlers.employee import router as employee_router
from handlers.manager import router as manager_router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    await init_db()

    # Роутерларни қўшиш
    dp.include_router(start_router)
    dp.include_router(employee_router)
    dp.include_router(manager_router)

    # Ботни ишга тушириш
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())