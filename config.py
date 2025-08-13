import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
support_group_id = int(os.getenv("SUPPORT_GROUP_ID"))
admin = int(os.getenv("ADMIN"))
