import httpx


def create_async_client():
    async with httpx.AsyncClient() as client:
        yield client


