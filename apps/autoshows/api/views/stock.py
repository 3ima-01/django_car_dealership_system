from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.autoshows.api.serializers.stock import StockSerializer
from apps.autoshows.models import Stock
from apps.autoshows.services.stock import AutoShowsStockService


class AutoShowsStockViewSet(
    ListModelMixin,
    GenericViewSet,
):
    queryset = Stock.objects.none()
    permission_classes = [IsAdminUser]
    serializer_class = StockSerializer

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = AutoShowsStockService()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

    @swagger_auto_schema(
        tags=["AutoShows Stock"],
        responses={200: StockSerializer(many=True)},
    )
    def list(self, request: Request, **kwargs) -> Response:
        autoshow_id = self.kwargs.get("autoshow_pk")
        if not autoshow_id:
            raise ValidationError("pk is required")

        stock = self.service.get_active_or_404(autoshow_id=autoshow_id)
        serializer = self.get_serializer(stock)
        return Response(serializer.data)
