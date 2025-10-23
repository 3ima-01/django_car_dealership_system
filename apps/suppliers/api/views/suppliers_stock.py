from typing import Any
from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.suppliers.api.serializers.suppliers_stock import (
    SuppliersStockCreateSerializer,
    SuppliersStockPublicSerializer,
    SuppliersStockUpdateSerializer,
)
from apps.suppliers.services.suppliers_stock import SuppliersStockService


class SuppliersStockAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = SuppliersStockService()

    @swagger_auto_schema(responses={200: SuppliersStockPublicSerializer(many=True)}, tags=["suppliers_stock"])
    def get(self, request: Request, id: UUID) -> Response:
        supplier_stock = self.service.get_supplier_stock(id)
        serializer = SuppliersStockPublicSerializer(supplier_stock, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=SuppliersStockCreateSerializer,
        responses={201: SuppliersStockPublicSerializer},
        tags=["suppliers_stock"],
    )
    def post(self, request: Request, id: UUID) -> Response:
        serializer = SuppliersStockCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            supplier_stock = self.service.add_car_to_supplier(serializer.validated_data)
            response_serializer = SuppliersStockPublicSerializer(supplier_stock)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=SuppliersStockUpdateSerializer, responses={204: "No Content"}, tags=["suppliers_stock"]
    )
    def patch(self, request: Request, id: UUID) -> Response:
        serializer = SuppliersStockUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            updated = self.service.update_supplier_car(id, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={204: "No Content"}, tags=["suppliers_stock"])
    def delete(self, request: Request, id: UUID) -> Response:
        deleted = self.service.delete_supplier_car(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
