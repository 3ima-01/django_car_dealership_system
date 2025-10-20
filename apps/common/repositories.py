class BaseRepository:
    model = None

    def get_all(self) -> list[model]:
        return self.model.objects.all()
