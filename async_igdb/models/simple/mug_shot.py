from datetime import datetime
from typing import Union
from ..base import BaseApiModel, ids
from ...util.enums import *


class CharacterMugShotModel(BaseApiModel):
    type = "character_mug_shots"
    searchable = False

    alpha_channel: bool = False
    animated: bool = False
    checksum: str | None = None
    height: int = 0
    image_id: str | None = None
    url: str | None = None
    width: int = 0