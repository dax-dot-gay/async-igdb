from .client import BaseClient
from .models import *
from .manager import ApiObjectManager


class IGDBClient(BaseClient):

    @property
    def characters(self) -> ApiObjectManager:
        return ApiObjectManager(self, CharacterModel)
