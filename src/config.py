import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

bot_token = os.getenv("BOT_TOKEN")
support_group_id = int(os.getenv("SUPPORT_GROUP_ID"))
admin = int(os.getenv("ADMIN"))
database_url = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR}/db/bot.db")
