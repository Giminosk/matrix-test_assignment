import pytest
from httpx import AsyncClient

from matrix_traversal.utils import (
    get_http_response,
    parse_response_to_matrix,
    traverse_matrix,
)
from matrix_traversal.exceptions import HTTPException


SOURCE_URL = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
UNSUPPORTED_URL = "httpsS://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
INVALID_URL = "https://😇"
RESPONSE_CODE_ERROR_URL = "https://httpbin.org/status/404"
TIMEOUT_URL = "https://google.com:1"
MATRIX = [[10, 20, 30, 40], [50, 60, 70, 80], [90, 100, 110, 120], [130, 140, 150, 160]]
TRAVERSAL = [10, 50, 90, 130, 140, 150, 160, 120, 80, 40, 30, 20, 60, 100, 110, 70]
with open("tests/example.txt", "r") as f:
    RESPONSE = f.read()


@pytest.mark.asyncio
@pytest.mark.parametrize("url, expected", [(SOURCE_URL, RESPONSE)])
async def test_get_http_response(url, expected):
    """
    Test to get the response from a given url in async mode.
    Args:
        url (_type_): url to request.
        expected (_type_): expected response.
    """
    async with AsyncClient() as client:
        response = await get_http_response(url=url, client=client)
        assert response == RESPONSE


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "invalid_url, exception",
    [
        (UNSUPPORTED_URL, f"Unsupported protocol: {UNSUPPORTED_URL}"),
        (INVALID_URL, f"Invalid URL: {INVALID_URL}"),
        (RESPONSE_CODE_ERROR_URL, "Server error: 404"),
        (TIMEOUT_URL, f"Failed to get response from {TIMEOUT_URL}"),
    ],
)
async def test_get_http_response_exceptions(invalid_url, exception):
    """
    Test to test the exceptions raised by the get_http_response function.
    Args:
        invalid_url (_type_): _description_
        exception (_type_): _description_
    """
    try:
        async with AsyncClient() as client:
            _ = await get_http_response(url=invalid_url, client=client)
    except HTTPException as e:
        assert str(e) == exception


@pytest.mark.asyncio
@pytest.mark.parametrize("response, matrix", [(RESPONSE, MATRIX)])
async def test_parse_response_to_matrix(response, matrix):
    """
    Test to test the parse_response_to_matrix function.
    Args:
        response (_type_): response from url to parse.
        matrix (_type_): parsed response as matrix.
    """
    assert await parse_response_to_matrix(response=response) == matrix


@pytest.mark.asyncio
@pytest.mark.parametrize("matrix, traversal", [(MATRIX, TRAVERSAL)])
async def test_traverse_matrix(matrix, traversal):
    """
    Test to test the traverse_matrix function.
    Args:
        matrix (_type_): matrix to traverse.
        traversal (_type_): expected traversal.
    """
    assert await traverse_matrix(matrix=matrix) == traversal
