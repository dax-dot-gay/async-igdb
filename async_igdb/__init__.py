from .client import BaseClient
from .models import *
from . import models
from .manager import ApiObjectManager


class IGDBClient(BaseClient):
    REGISTRY: dict[str, BaseApiModel] = {
        getattr(models, model).type: getattr(models, model)
        for model in [
            i for i in dir(models) if i.endswith("Model") and i != "BaseApiModel"
        ]
    }

    @property
    def characters(self) -> ApiObjectManager[CharacterModel]:
        return ApiObjectManager[CharacterModel](self, CharacterModel)

    @property
    def games(self) -> ApiObjectManager[GameModel]:
        return ApiObjectManager[GameModel](self, GameModel)

    @property
    def collections(self) -> ApiObjectManager[CollectionModel]:
        return ApiObjectManager[CollectionModel](self, CollectionModel)

    @property
    def companies(self) -> ApiObjectManager[CompanyModel]:
        return ApiObjectManager[CompanyModel](self, CompanyModel)
