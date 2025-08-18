from aiogram import Bot

from middlewares import logger


async def broadcast_message_to_users(
        bot: Bot,
        user_ids: list[int],
        text: str,
        parse_mode: str = "HTML"
) -> tuple[int, int]:
    """
    Makes a message sent to a list of users.
    Returns a tuple (successfully_sent, unsuccessfully_sent).
    """

    sent_count = 0
    failed_count = 0

    for user_id in user_ids:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=text,
                parse_mode=parse_mode
            )
            sent_count += 1

        except Exception as e:
            logger.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
            failed_count += 1

    return sent_count, failed_count
