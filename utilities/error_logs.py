from pathlib import Path
import aiofiles
from middlewares import logger


def get_filtered_logs(logs: list[str]) -> list[str]:
    """Returns only logs with levels ERROR, WARNING or DEBUG."""
    filtered_logs = []
    level_logs = ["ERROR", "WARNING", "DEBUG"]

    for line in logs:
        if any(level in line for level in level_logs):
            filtered_logs.append(line)

    return filtered_logs


async def read_log_file(file_path: Path) -> list[str]:
    """Reads log file"""
    try:
        if not file_path.exists():
            logger.debug(f"Файл логов не найден")
            return []

        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            logs = f.readlines()
            return await logs

    except Exception as e:
        logger.error(f"Ошибка при чтении логов: {e}")
        return []


def get_last_filtered_line(logs: list[str], count: int = 10) -> str | None:
    """Return last 10 filtered line in log file"""
    filtered = get_filtered_logs(logs)
    if not filtered:
        logger.debug("Нет логов уровня ERROR/WARNING/DEBUG")
        return ""
    return "".join(filtered[-count:])


async def get_error_logs() -> str:
    """Main point to get error logs"""
    log_file = Path("logs/bot.log")
    logs = await read_log_file(log_file)
    return get_last_filtered_line(logs)
