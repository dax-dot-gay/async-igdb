import math
from typing import Annotated, ClassVar, Literal, Type, TypeVar, get_type_hints
from pydantic import BaseModel
from ..client import BaseClient

TBase = TypeVar("TBase", bound="BaseApiModel")


class IDWrapper:
    def __init__(self, factory: TBase | str):
        self.factory = factory

    async def resolve(
        self, client: BaseClient, ids: list[int], step: int = 100
    ) -> list[TBase]:
        results = []
        if type(self.factory) == str:
            _type = self.factory
        else:
            _type = self.factory.type
        for i in range(0, math.ceil(len(ids) / step)):
            results.extend(
                await client.build_query(_type, ids=ids, limit=step, offset=step * i)
            )

        return results


def ids(base: Type[TBase] | str):
    return Annotated[list[int] | int, IDWrapper(base)]


class BaseApiModel(BaseModel):
    type: ClassVar[str | None] = None
    searchable: ClassVar[bool] = False
    fields: ClassVar[list[str] | Literal["*"]] = "*"
    _client: BaseClient

    id: int

    def __init__(self, client: BaseClient = None, **data):
        super().__init__(**data)
        if client:
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

    @property
    def client(self):
        return self._client

    @property
    def id_fields(self) -> dict[str, IDWrapper]:
        hints = get_type_hints(
            self,
            include_extras=True,
            globalns=dict(
                **globals(), **{v.__name__: v for v in self.client.REGISTRY.values()}
            ),
        )
        fields: dict[str, IDWrapper] = {}
        for key, value in hints.items():
            if getattr(value, "__name__", None) == "Annotated" and hasattr(
                value, "__metadata__"
            ):
                for i in value.__metadata__:
                    if isinstance(i, IDWrapper):
                        fields[key] = i

            if getattr(value, "__name__", None) == "Union":
                for i in value.__args__:
                    if getattr(i, "__name__", None) == "Annotated" and hasattr(
                        i, "__metadata__"
                    ):
                        for j in i.__metadata__:
                            if isinstance(j, IDWrapper):
                                fields[key] = j
                                break

        return fields

    async def resolve_links(self, fields: list[str] | None = None):
        if fields:
            to_resolve = {}
            for field, wrapper in self.id_fields.items():
                if field in fields:
                    to_resolve[field] = wrapper
        else:
            to_resolve = self.id_fields

        result = self.model_dump()
        for field, wrapper in to_resolve.items():
            if hasattr(self, field):
                if getattr(self, field) == None:
                    resolved = None
                else:
                    if type(getattr(self, field)) == int:
                        resolved = await wrapper.resolve(
                            self.client, [getattr(self, field)]
                        )
                    else:
                        if len(getattr(self, field, [])) > 0:
                            resolved = await wrapper.resolve(
                                self.client, getattr(self, field, [])
                            )
                        else:
                            resolved = []
            else:
                resolved = None

            result[field] = resolved

        return self.client.REGISTRY[self.type](self.client, **result)
