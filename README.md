# Python Test Assignment

## Task

You need to implement a Python library that asynchronous fetches a square matrix (NxN) from a remote server and returns it to the user as a `List[int]`. This list should contain the result of traversing the received matrix in a counterclockwise spiral manner, starting from the top-left corner.

- The function takes a single argument, which is the URL to fetch the matrix from the server using HTTP(S) protocol.
- The function returns a list containing the result of traversing the received matrix in a counterclockwise spiral manner, starting from the top-left corner.
- Interaction with the server should be implemented asynchronously using aiohttp, httpx, or another asyncio component.
- The library should handle server errors and network errors correctly (5xx, Connection Timeout, Connection Refused, etc.).
- In the future, the dimension of the matrix may change while preserving the formatting. The library should remain functional for square matrices of different dimensions.