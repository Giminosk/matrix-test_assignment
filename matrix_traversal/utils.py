from httpx import AsyncClient
from httpx import HTTPStatusError, TimeoutException, InvalidURL, UnsupportedProtocol

from matrix_traversal.config import logger


async def get_http_response(url: str, client: AsyncClient) -> str:
    try:
        response = await client.get(url)
    except UnsupportedProtocol as e:
        logger.error(f"{e}")
        raise Exception(f"Unsupported protocol: {url}")
    except InvalidURL as e:
        logger.error(f"{e}")
        raise Exception(f"Invalid URL: {url}")
    except HTTPStatusError as e:
        logger.error(f"{e}")
        raise Exception(f"Server error: {response.status_code}")
    except TimeoutException as e:
        logger.error(f"{e}")
        raise Exception(f"Failed to get response from {url}")

    return response.content.decode()


async def parse_response_to_matrix(response: str) -> list[list[int]]:
    matrix = []
    for line in response.split("\n"):
        if line and not line.startswith("+"):
            matrix.append([int(num) for num in line.split("|")[1:-1]])

    if any([len(row) != len(matrix) for row in matrix]):
        logger.error("Matrix is not square")

    return matrix


async def traverse_matrix(matrix: list[list[int]]) -> list[int]:
    result = []
    while matrix:
        result.extend(matrix.pop(0))
        matrix = list(zip(*matrix))[::-1]
    return result
