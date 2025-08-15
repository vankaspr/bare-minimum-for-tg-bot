import asyncio
from database import engine, Base
from handlers.admin import admin_router, auxiliary_router
from handlers.users import router, support_router
from settings import dp, bot
from settings.middlewares import logger
from settings.middlewares.db_session_middleware import DBSessionMiddleware
from utilities import set_commands


async def init_database():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Таблицы БД успешно созданы/проверены")
    except Exception as e:
        logger.critical(f"❌ Ошибка подключения к БД: {e}")
        raise


async def main():

    await init_database()

    dp.update.middleware(DBSessionMiddleware())

    dp.include_router(router=router)
    dp.include_router(router=support_router)
    dp.include_router(router=admin_router)
    dp.include_router(router=auxiliary_router)

    await set_commands()

    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("✅ Бот успешно запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":

    logger.info("🔁 Бот запускается...")

    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"🆘 Ошибка при запуске бота: {e}")
