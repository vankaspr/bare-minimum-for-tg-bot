import asyncio

from core.config import dp, bot, logger
from core.routers import router


async def main():
    dp.include_router(router=router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Start YoBa↗️")
    asyncio.run(main())
