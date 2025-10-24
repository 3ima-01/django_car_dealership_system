from typing import Any
from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.autoshows.api.serializers.autoshows_stock import (
    AutoShowsStockPublicSerializer,
)
from apps.autoshows.services.autoshows_stock import AutoShowsStockService


class AutoShowsStockAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = AutoShowsStockService()

    @swagger_auto_schema(responses={200: AutoShowsStockPublicSerializer(many=True)}, tags=["autoshows_stock"])
    def get(self, request: Request, id: UUID) -> Response:
        stock = self.service.get_autoshow_stock(id)
        serializer = AutoShowsStockPublicSerializer(stock, many=True)
        return Response(serializer.data)
