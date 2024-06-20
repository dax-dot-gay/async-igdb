from datetime import datetime
from typing import Union
from ..base import BaseApiModel, ids
from .age_rating import AgeRatingModel
from ..simple import *
from ...util.enums import *


class GameModel(BaseApiModel):
    type = "games"
    searchable = True

    age_ratings: ids(AgeRatingModel) = []
    aggregated_rating: float = 0.0
    aggregated_rating_count: int = 0
    alternative_names: ids(AlternativeNameModel) = []
    artworks: ids(ArtworkModel) = []
    bundles: ids("games") | list["GameModel"] = []
    category: GameCategoryEnum = GameCategoryEnum.main_game
    collection: int | None = None
    collections: list[int] = []
    cover: int | None = None
    dlcs: ids("games") | list["GameModel"] = []
    expanded_games: ids("games") | list["GameModel"] = []
    expansions: ids("games") | list["GameModel"] = []
    external_games: list[int] = []
    first_release_date: datetime | None = None
    forks: ids("games") | list["GameModel"] = []
    franchise: int | None = None
    franchises: list[int] = []
    game_engines: list[int] = []
    game_localizations: list[int] = []
    game_modes: list[int] = []
    genres: list[int] = []
    involved_companies: list[int] = []
    multiplayer_modes: list[int] = []
    name: str | None = None
    parent_game: Union[ids("games"), "GameModel", None] = None
    platforms: list[int] = []
    player_perspectives: list[int] = []
    ports: ids("games") | list["GameModel"] = []
    rating: float = 0.0
    rating_count: int = 0
    release_dates: list[int] = []
    remakes: ids("games") | list["GameModel"] = []
    remasters: ids("games") | list["GameModel"] = []
    screenshots: list[int] = []
    similar_games: ids("games") | list["GameModel"] = []
    slug: str | None = None
    standalone_expansions: ids("games") | list["GameModel"] = []
    status: GameStatusEnum | None = None
    storyline: str | None = None
    summary: str | None = None
    tags: list[int] = []
    themes: list[int] = []
    total_rating: float = 0.0
    total_rating_count: int = 0
    version_parent: Union[ids("games"), "GameModel", None] = None
    version_title: str | None = None
    videos: list[int] = []
    websites: list[int] = []
