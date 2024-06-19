import asyncio
import json
from dotenv import load_dotenv
import os
from async_igdb import IGDBClient
from async_igdb.util import CharacterSpeciesEnum

load_dotenv()


async def main():
    client_id = os.getenv("IGDB_ID")
    client_secret = os.getenv("IGDB_SECRET")

    async with IGDBClient(client_id, client_secret=client_secret) as client:
        async for result in client.characters.find_all(search="Mario"):
            print(result)


asyncio.run(main())
