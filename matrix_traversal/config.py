from loguru import logger
from httpx import AsyncClient
from pathlib import Path

Path("../app.log").touch()
logger.remove()
logger.add("../app.log", rotation="1 day", retention="7 days", level="INFO")


async def create_async_client() -> AsyncClient:
    client = AsyncClient()
    return client
