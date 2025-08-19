from aiogram.types import BotCommand, BotCommandScopeDefault
from src.settings import bot
from src.core.middlewares import logger


async def set_commands():
    cmd = [
        BotCommand(command="start", description="hi-message"),
        BotCommand(command="support", description="supporter"),
        BotCommand(command="help", description="commands list"),
    ]
    logger.info("Устанавливаем команды для бота...")
    await bot.set_my_commands(cmd, BotCommandScopeDefault())
