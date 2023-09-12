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
    try:
        async with AsyncClient() as client:
            _ = await get_http_response(url=invalid_url, client=client)
    except HTTPException as e:
        assert str(e) == exception


@pytest.mark.asyncio
@pytest.mark.parametrize("response, matrix", [(RESPONSE, MATRIX)])
async def test_parse_response_to_matrix(response, matrix):
    assert await parse_response_to_matrix(response=response) == matrix


@pytest.mark.asyncio
@pytest.mark.parametrize("matrix, traversal", [(MATRIX, TRAVERSAL)])
async def test_traverse_matrix(matrix, traversal):
    assert await traverse_matrix(matrix=matrix) == traversal
