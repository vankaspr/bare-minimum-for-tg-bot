import asyncio

from handlers.admin import admin_router, auxiliary_router
from handlers.users import router, support_router
from settings import dp, bot
from settings.middlewares import logger
from utilities import set_commands


async def main():
    dp.include_router(router=router)
    dp.include_router(router=support_router)
    dp.include_router(router=admin_router)
    dp.include_router(router=auxiliary_router)
    await set_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":

    logger.info("🔁 Бот запускается...")

    try:
        logger.info("✅ Бот успешно запущен!")
        asyncio.run(main())
    except Exception as e:
        logger.error(f"🆘 Ошибка при запуске бота: {e}")
