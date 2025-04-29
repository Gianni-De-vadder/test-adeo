import pytest
import httpx
import httpcore
from unittest.mock import AsyncMock, patch

from utils import resilient_get

@pytest.mark.asyncio
async def test_retry_success_on_second_attempt():
    mock_get = AsyncMock(side_effect=[
        httpcore.ConnectError("First fail"),
        httpcore.ConnectError("Second fail"),
        httpx.Response(200)
    ])

    with patch("httpx.AsyncClient.get", mock_get):
        response = await resilient_get("https://google.com")
        assert response.status_code == 200
        assert mock_get.call_count == 3

@pytest.mark.asyncio
async def test_retry_raises_after_max_retries():
    mock_get = AsyncMock(side_effect=httpcore.ConnectError("Always fails"))

    with patch("httpx.AsyncClient.get", mock_get):
        with pytest.raises(httpcore.ConnectError):
            await resilient_get("https://google.com")
        assert mock_get.call_count == 3
