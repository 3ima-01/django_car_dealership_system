from apps.autoshows.models import AutoShows
from apps.common.repositories import BaseRepository


class AutoShowsRepository(BaseRepository[AutoShows]):
    model = AutoShows
