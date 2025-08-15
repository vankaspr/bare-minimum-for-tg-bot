from datetime import datetime
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from typing import Union, Dict
from settings.middlewares import logger


class AdminFilter(BaseFilter):
    def __init__(
            self,
            admin_ids: Union[int, list[int], Dict[int, str]],
            max_attempts: int = 3
    ):
        """
        :param admin_ids: ID админов (int, list[int] или dict[id, имя])
        :param max_attempts: Макс. попыток доступа перед блокировкой
        """
        if isinstance(admin_ids, dict):
            self.admin_ids = list(admin_ids.keys())
        elif isinstance(admin_ids, int):
            self.admin_ids = [admin_ids]
        else:
            self.admin_ids = admin_ids

        self.max_attempts = max_attempts
        self.access_attempts = {}

    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        user = update.from_user
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        if user.id in self.admin_ids:
            logger.info(f"Доступ разрешён для администратора {user.id} ({user.username})")
            return True


        self._log_access_attempt(user, current_time)


        if self._check_access_attempts(user.id):
            logger.warning(f"Блокировка доступа для пользователя {user.id} - превышено кол-во попыток")
            if isinstance(update, CallbackQuery):
                await update.answer("🚫 Доступ заблокирован!", show_alert=True)
            else:
                await update.answer("⚠️ Доступ к этой команде заблокирован")
            return False


        if isinstance(update, CallbackQuery):
            await update.answer("🔐 Доступ запрещён", show_alert=True)
        else:
            await update.answer("⚠️ У вас нет прав доступа к этой команде")
        return False

    def _log_access_attempt(self, user, timestamp):
        attempt_info = {
            'user_id': user.id,
            'username': user.username,
            'timestamp': timestamp
        }

        logger.warning(f"Попытка доступа неавторизованного пользователя: {attempt_info}")

        if user.id not in self.access_attempts:
            self.access_attempts[user.id] = []
        self.access_attempts[user.id].append(timestamp)

    def _check_access_attempts(self, user_id: int) -> bool:
        if user_id not in self.access_attempts:
            return False

        current_time = datetime.now()
        self.access_attempts[user_id] = [
            t for t in self.access_attempts[user_id]
            if (current_time - datetime.strptime(t, "%Y-%m-%d %H:%M:%S")).total_seconds() < 3600
        ]

        return len(self.access_attempts[user_id]) >= self.max_attempts

    def check_user_id(self, user_id: int) -> bool:
        return user_id in self.admin_ids
