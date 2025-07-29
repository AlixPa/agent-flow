import asyncio
from logging import Logger
from typing import AsyncGenerator

from src.logger import get_logger

from .models import StreamMessage

base_logger = get_logger()


class Messenger:
    def __init__(self, logger: Logger | None = None):
        self.logger = logger or base_logger
        self.queue: asyncio.Queue[StreamMessage] = asyncio.Queue()

    async def send(self, message: StreamMessage):
        await self.queue.put(message)

    async def stream(self) -> AsyncGenerator[str, None]:
        try:
            while True:
                msg = await self.queue.get()
                yield msg.model_dump_json()
                if msg.is_final_message:
                    break
        except asyncio.CancelledError:
            pass  # Client disconnected
