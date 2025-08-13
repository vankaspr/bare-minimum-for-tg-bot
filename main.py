import asyncio

from handlers.users import router, support_router
from settings import dp, bot
from settings.middlewares import logger


async def main():
    dp.include_router(router=router)
    dp.include_router(router=support_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Start YoBa↗️")
    asyncio.run(main())
