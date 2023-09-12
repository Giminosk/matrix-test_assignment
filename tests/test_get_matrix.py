import pytest
from matrix_traversal import get_matrix


SOURCE_URL = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
TRAVERSAL = [10, 50, 90, 130, 140, 150, 160, 120, 80, 40, 30, 20, 60, 100, 110, 70]


@pytest.mark.asyncio
@pytest.mark.parametrize("url, traversed_matrix", [(SOURCE_URL, TRAVERSAL)])
async def test_get_matrix(url, traversed_matrix):
    assert await get_matrix(url) == traversed_matrix
