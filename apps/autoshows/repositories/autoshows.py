from apps.autoshows.models import AutoShows
from apps.common.repositories import BaseRepository


class AutoShowsNotFoundException(Exception):
    """Исключение, выбрасываемое когда автосалон не найден"""

    pass


class AutoShowsRepository(BaseRepository):
    model = AutoShows
