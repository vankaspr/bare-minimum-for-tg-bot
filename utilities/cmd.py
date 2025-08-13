from aiogram.types import BotCommand, BotCommandScopeDefault
from settings import bot
from settings.middlewares import logger


async def set_commands():
    cmd = [
        BotCommand(command="start", description="hi-message"),
        BotCommand(command="support", description="supporter"),

    ]
    logger.info("Set commands...")
    await bot.set_my_commands(cmd, BotCommandScopeDefault())