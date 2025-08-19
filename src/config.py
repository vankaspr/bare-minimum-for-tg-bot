import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

DB_DIR = BASE_DIR / "data" / "db"
LOG_DIR = BASE_DIR / "data" / "logs"

DB_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DB_DIR / "bot.db"

bot_token = os.getenv("BOT_TOKEN")
support_group_id = int(os.getenv("SUPPORT_GROUP_ID"))
admin = int(os.getenv("ADMIN"))
database_url = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{DB_PATH}")

