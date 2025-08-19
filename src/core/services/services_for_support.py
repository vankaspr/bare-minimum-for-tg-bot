from datetime import datetime
from aiogram.types import User, Message
from src.config import support_group_id
from src.settings import bot
from src.core.middlewares import logger


async def format_support_message(user: User, issue: str) -> str:
    """Formats a message for sending to support."""
    current_time = datetime.now().strftime("%d.%m.%Y, %H:%M")
    return (
        f"⚠️ <b>Support</b> | New request\n\n"
        f"👤 From: @{user.username}\n\n"
        f"🆔 : <code>{user.id}</code>\n\n"
        f"📅 Date: {current_time}\n\n"
        f"<b>📩 Issue:</b>\n\n"
        f"<blockquote>{issue}</blockquote>"
    )


async def process_support_message(
    message: Message,
):
    """Process user support request"""
    try:
        from src.core.keyboards import support_kb

        logger.info("Обработка запроса в поддержку")
        support_message = await format_support_message(message.from_user, message.text)

        await bot.send_message(
            chat_id=support_group_id, text=support_message, parse_mode="HTML"
        )
        await message.answer(
            "Перенаправили ваш запрос в тех.поддержку!\n"
            "Решим проблему как только, так сразу 😇",
            reply_markup=support_kb(),
        )

        return True

    except Exception as e:
        logger.error(f"Не получилось отправить запрос в поддержку: {e}")
        await message.answer(
            "Произошла ошибка при отправке запроса.\n" "Пожалуйста, попробуйте позже."
        )
        return False
