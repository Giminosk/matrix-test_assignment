from matrix_traversal.config import create_async_client
from matrix_traversal.utils import (
    get_http_response,
    parse_response_to_matrix,
    traverse_matrix,
)


async def get_matrix(url: str) -> list[int]:
    client = await create_async_client()

    async with await create_async_client() as client:
        response = await get_http_response(url, client)
        matrix = await parse_response_to_matrix(response)
        traversed_matrix = await traverse_matrix(matrix)

    return traversed_matrix
