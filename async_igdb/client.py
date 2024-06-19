import asyncio
from contextlib import asynccontextmanager
from typing import Any, Literal, TypeVar

from httpx import AsyncClient

TSelf = TypeVar("TSelf", bound="BaseClient")
BASE_URL = "https://api.igdb.com/v4/{endpoint}"


class BaseClient:
    def __init__(
        self, client_id: str, access_token: str = None, client_secret: str = None
    ):
        self.client_id = client_id
        if (access_token and client_secret) or (not access_token and not client_secret):
            raise ValueError(
                "Exactly one of access_token OR client_secret must be specified."
            )

        if access_token:
            self.auth_mode = "token"
            self.access_token = access_token
            self.client_secret = None
        else:
            self.auth_mode = "secret"
            self.client_secret = client_secret
            self.access_token = None

        self.client = None
        self.refresh_task = None

    async def _schedule_refresh(self, expire: int, buffer: int = 1800):
        await asyncio.sleep(expire - buffer)
        await self._get_token()

    async def _get_token(self):
        if self.auth_mode == "token":
            raise RuntimeError("Cannot get token w/o client secret")

        result = await self.client.post(
            "https://id.twitch.tv/oauth2/token",
            params={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
        )

        if result.is_success:
            data = result.json()
            self.refresh_task = asyncio.create_task(
                self._schedule_refresh(data["expires_in"])
            )
            self.access_token = data["access_token"]
        else:
            if self.refresh_task:
                self.refresh_task.cancel()
            self.refresh_task = None
            raise ConnectionError("Failed to refresh access token")

    async def __aenter__(self: TSelf) -> TSelf:
        self.client = AsyncClient()
        if self.auth_mode == "secret":
            await self._get_token()

        self.client.headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
        }

        return self

    async def __aexit__(self, *args):
        await self.client.aclose()
        if self.refresh_task:
            self.refresh_task.cancel()

    async def request(
        self,
        endpoint: str,
        fields: Literal["*"] | list[str] = "*",
        queries: list[str] = [],
    ) -> dict[str, Any]:
        result = await self.client.post(
            BASE_URL.format(endpoint=endpoint.lstrip("/")),
            headers={"Accept": "application/json"},
            data=f"fields {'*' if fields == '*' else ','.join(fields)};{' ' + '; '.join(queries) + ';' if len(queries) > 0 else ''}",
        )
        result.raise_for_status()
        return result.json()