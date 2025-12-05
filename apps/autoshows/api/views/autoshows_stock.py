from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.autoshows.api.serializers.autoshows_stock import AutoShowsStockSerializer
from apps.autoshows.models import AutoShowsStock
from apps.autoshows.services.autoshows_stock import AutoShowsStockService


class AutoShowsStockViewSet(
    ListModelMixin,
    GenericViewSet,
):
    queryset = AutoShowsStock.objects.none()
    permission_classes = [AllowAny]
    serializer_class = AutoShowsStockSerializer

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = AutoShowsStockService()

    @swagger_auto_schema(
        tags=["AutoShows"],
        responses={200: AutoShowsStockSerializer(many=True)},
    )
    def list(self, request: Request, **kwargs) -> Response:
        autoshow_id = self.kwargs.get("autoshow_id")
        if not autoshow_id:
            raise ValidationError("autoshow_id is required")

        stock = self.service.get_autoshow_stock(autoshow_id)
        serializer = self.get_serializer(stock, many=True)
        return Response(serializer.data)
