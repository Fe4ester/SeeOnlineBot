from aiogram.filters import BaseFilter
from aiogram.types import Message


class CommandOrTextFilter(BaseFilter):
    def __init__(self, command=None, text_contains=None):
        self.command = command
        self.text_contains = text_contains

    async def __call__(self, message: Message):
        if not message.text:
            return False

        if self.command and message.text.startswith(f"/{self.command}"):
            return True

        if self.text_contains and self.text_contains in message.text:
            return True

        return False
