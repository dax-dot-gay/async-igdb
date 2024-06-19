from .client import BaseClient
from .models import *
from .manager import ApiObjectManager


class IGDBClient(BaseClient):
    REGISTRY = {"characters": CharacterModel, "games": GameModel}

    @property
    def characters(self) -> ApiObjectManager[CharacterModel]:
        return ApiObjectManager[CharacterModel](self, CharacterModel)

    @property
    def games(self) -> ApiObjectManager[GameModel]:
        return ApiObjectManager[GameModel](self, GameModel)
