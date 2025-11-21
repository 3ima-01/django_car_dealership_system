from typing import Any
from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.suppliers.api.serializers.suppliers_stock import (
    SuppliersStockCreateSerializer,
    SuppliersStockPublicSerializer,
    SuppliersStockUpdateSerializer,
)
from apps.suppliers.services.suppliers_stock import SuppliersStockService


class SuppliersStockViewSet(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [AllowAny]
    serializer_class = SuppliersStockPublicSerializer

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = SuppliersStockService()

    def get_queryset(self):
        from apps.suppliers.models import SuppliersStock

        return SuppliersStock.objects.none()

    @swagger_auto_schema(
        tags=["Suppliers"],
        responses={200: SuppliersStockPublicSerializer(many=True)},
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        supplier_id = self.kwargs.get("supplier_id")
        if not supplier_id:
            raise ValidationError("supplier_id is required")
        stock = self.service.get_supplier_stock(supplier_id)
        serializer = self.get_serializer(stock, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Suppliers"],
        request_body=SuppliersStockCreateSerializer,
        responses={201: SuppliersStockPublicSerializer},
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        supplier_id = self.kwargs.get("supplier_id")
        serializer = SuppliersStockCreateSerializer(data={**request.data, "supplier_id": supplier_id})
        serializer.is_valid(raise_exception=True)
        stock_item = self.service.add_car_to_supplier(serializer.validated_data)
        response_serializer = SuppliersStockPublicSerializer(stock_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Suppliers"],
        request_body=SuppliersStockUpdateSerializer,
        responses={204: "No Content"},
    )
    def partial_update(self, request: Request, pk: UUID, *args, **kwargs) -> Response:
        serializer = SuppliersStockUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.update_supplier_car(pk, serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=["Suppliers"],
        responses={204: "No Content"},
    )
    def destroy(self, request: Request, pk: UUID, *args, **kwargs) -> Response:
        self.service.delete_supplier_car(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
