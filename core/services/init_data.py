from pathlib import Path
import os

from core.middlewares import logger


def init_data_directories(
        base_data_path: Path = None
):
    if base_data_path is None:
        base_data_path = Path(__file__).parent.parent.parent.parent / "data"

    directories = [
        base_data_path / "db",
        base_data_path / "logs"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info("f✅ Создана директория: {directory}")

    return base_data_path