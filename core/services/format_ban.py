from database.models import BanRecord


def format_ban_list(ban_list: list[tuple[BanRecord, str]]) -> str:
    """Formats the ban list into a readable text message"""
    if not ban_list:
        return "Список активных банов пуст"

    message = "📋 Список активных банов:\n\n"
    for ban, username in ban_list:
        message += (
            f"👤 @{username} (ID: {ban.user_id})\n"
            f"📅 {ban.ban_date.strftime('%d.%m.%Y %H:%M')}\n"
            f"📌 Причина: {ban.ban_reason}\n"
            f"🛡 Забанил: {ban.banned_by}\n"
            f"──────────────────\n"
        )
    return message
