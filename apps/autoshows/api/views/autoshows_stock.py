from typing import Any
from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.autoshows.api.serializers.autoshows_stock import (
    AutoShowsStockPublicSerializer,
)
from apps.autoshows.services.autoshows_stock import AutoShowsStockService


class AutoShowsStockViewSet(
    ListModelMixin,
    GenericViewSet,
):
    permission_classes = [AllowAny]
    serializer_class = AutoShowsStockPublicSerializer

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = AutoShowsStockService()

    def get_queryset(self):
        from apps.autoshows.models import AutoShowsStock

        return AutoShowsStock.objects.none()

    @swagger_auto_schema(
        tags=["AutoShows"],
        responses={200: AutoShowsStockPublicSerializer(many=True)},
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        autoshow_id = self.kwargs.get("autoshow_id")
        if not autoshow_id:
            raise ValidationError("autoshow_id is required")

        stock = self.service.get_autoshow_stock(autoshow_id)
        serializer = self.get_serializer(stock, many=True)
        return Response(serializer.data)
