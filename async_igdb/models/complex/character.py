from datetime import datetime
from ..base import BaseApiModel
from ...util.enums import *


class CharacterModel(BaseApiModel):
    type = "characters"
    searchable = True

    akas: list[str] = []
    checksum: str | None = None
    country_name: str | None = None
    created_at: datetime | None = None
    description: str | None = None
    games: list[int] = []
    gender: CharacterGenderEnum = CharacterGenderEnum.Other
    mug_shot: int | None = None
    name: str | None = None
    slug: str | None = None
    species: CharacterSpeciesEnum = CharacterSpeciesEnum.Unknown
    updated_at: datetime | None = None
    url: str | None = None
