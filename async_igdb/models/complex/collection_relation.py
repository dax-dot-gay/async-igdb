from datetime import datetime
from typing import Union

from pydantic import Field
from ..base import BaseApiModel, ids
from ...util.enums import *
from .collection_relation_type import CollectionRelationTypeModel


class CollectionRelationModel(BaseApiModel):
    type = "collection_relations"
    searchable = False

    checksum: str | None = None
    child_collection: int | None = None
    created_at: datetime | None = None
    parent_collection: int | None = None
    relation_type: ids(CollectionRelationTypeModel) = Field(default=None, alias="type")
