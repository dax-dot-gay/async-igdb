from typing import ClassVar, Literal, Type, TypeVar
from pydantic import BaseModel
from ..client import BaseClient

TBase = TypeVar("TBase", bound="BaseApiModel")


class BaseApiModel(BaseModel):
    type: ClassVar[str | None] = None
    searchable: ClassVar[bool] = False
    fields: ClassVar[list[str] | Literal["*"]] = "*"
    _client: BaseClient

    id: int

    def __init__(self, client: BaseClient, **data):
        super().__init__(**data)
        self._client = client

    @classmethod
    async def from_request(
        cls: Type[TBase],
        client: BaseClient,
        ids: list[int] | None = None,
        filter: str | None = None,
        sort_field: str | None = None,
        sort_direction: Literal["asc", "desc"] = "asc",
        search: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[TBase]:
        if search and not cls.searchable:
            raise ValueError("This model is non-searchable.")
        result = await client.build_query(
            cls.type,
            fields=cls.fields,
            ids=ids,
            filter=filter,
            sort_field=sort_field,
            sort_direction=sort_direction,
            limit=limit,
            offset=offset,
        )
        return [cls(client, **r) for r in result]
