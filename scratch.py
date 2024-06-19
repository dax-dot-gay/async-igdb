import asyncio
import json
from dotenv import load_dotenv
import os
from async_igdb import BaseClient

load_dotenv()


async def main():
    client_id = os.getenv("IGDB_ID")
    client_secret = os.getenv("IGDB_SECRET")

    async with BaseClient(client_id, client_secret=client_secret) as client:
        result = await client.request("/games", queries=['search "Mario Kart"'])
        print(json.dumps(result, indent=4))


asyncio.run(main())
