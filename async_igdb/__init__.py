from .client import BaseClient
from .models import *
from .manager import ApiObjectManager


class IGDBClient(BaseClient):
    REGISTRY = {
        "characters": CharacterModel,
        "games": GameModel,
        "character_mug_shots": CharacterMugShotModel,
        "age_ratings": AgeRatingModel,
        "collection_relation_types": CollectionRelationTypeModel,
        "collection_relations": CollectionRelationModel,
        "age_rating_content_descriptions": AgeRatingContentDescriptionModel,
        "alternative_names": AlternativeNameModel,
        "artworks": ArtworkModel,
        "collection_types": CollectionTypeModel,
        "collections": CollectionModel,
        "company_logos": CompanyLogoModel,
        "company_websites": CompanyWebsiteModel,
        "collection_memberships": CollectionMembershipModel,
        "collection_membership_types": CollectionMembershipTypeModel,
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
