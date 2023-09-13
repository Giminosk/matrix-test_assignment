from httpx import AsyncClient
from httpx import TimeoutException, InvalidURL, UnsupportedProtocol

from matrix_traversal.config import logger
from matrix_traversal.exceptions import HTTPException


async def get_http_response(url: str, client: AsyncClient) -> str:
    """
    Function to get HTTP response from URL in asynchronous way.
    Args:
        url (str): url to get HTTP response from.
        client (AsyncClient): AsyncClient instance.

    Raises:
        HTTPException: Unsupported protocol exception.
        HTTPException: Invalid URL exception.
        HTTPException: Timeout exception.
        HTTPException: Status code exception.

    Returns:
        str: _description_
    """
    try:
        response = await client.get(url)
    except UnsupportedProtocol as e:
        logger.error(f"{e}")
        raise HTTPException(f"Unsupported protocol: {url}")
    except InvalidURL as e:
        logger.error(f"{e}")
        raise HTTPException(f"Invalid URL: {url}")
    except TimeoutException as e:
        logger.error(f"{e}")
        raise HTTPException(f"Failed to get response from {url}")

    if 400 <= response.status_code < 600:
        logger.error(f"Server error: {response.status_code}")
        raise HTTPException(f"Server error: {response.status_code}")

    return response.content.decode()


async def parse_response_to_matrix(response: str) -> list[list[int]]:
    """
    Function to parse a string response to a matrix.
    Args:
        response (str): response got from url to parse

    Returns:
        list[list[int]]: parsed matrix.
    """
    matrix = []
    for line in response.split("\n"):
        if line and not line.startswith("+"):
            matrix.append([int(num) for num in line.split("|")[1:-1]])

    if any([len(row) != len(matrix) for row in matrix]):
        logger.error("Matrix is not square")

    return matrix


async def traverse_matrix(matrix: list[list[int]]) -> list[int]:
    """
    Function to traverse a matrix in spiral way.
    Args:
        matrix (list[list[int]]): matrix to traverse.

    Returns:
        list[int]: traversed matrix.
    """
    result = []
    matrix = list(zip(*matrix))
    while matrix:
        result.extend(matrix.pop(0))
        matrix = list(zip(*matrix))[::-1]
    return result


async def main(url):
    """
    Main function.
    """
    async with AsyncClient() as client:
        response = await get_http_response(url, client)
    print(response)
