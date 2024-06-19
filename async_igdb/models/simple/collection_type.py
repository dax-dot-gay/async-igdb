from datetime import datetime
from typing import Union
from ..base import BaseApiModel, ids
from ...util.enums import *


class CollectionTypeModel(BaseApiModel):
    type = "collection_types"
    searchable = False

    checksum: str | None = None
    created_at: datetime | None = None
    description: str | None = None
    name: str | None = None
    updated_at: datetime | None = None
