import httpx
import httpcore
import asyncio

async def resilient_get(url: str, max_retries: int = 2):
    attempts = 0
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response
        except httpcore.ConnectError as e:
            if attempts < max_retries:
                attempts += 1
                print(f"Retrying... attempt {attempts + 1}")
                await asyncio.sleep(0.5)
            else:
                raise e
