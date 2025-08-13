from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from typing import Union, List

class IsAdmin(BaseFilter):
    def __init__(self, user_id: Union[int, List[int]]):
        self.user_id = [user_id] if isinstance(user_id, int) else user_id

    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        return update.from_user.id in self.user_id