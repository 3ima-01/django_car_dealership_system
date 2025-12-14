from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.suppliers.api.serializers.stock import StockSerializer
from apps.suppliers.models import Stock
from apps.suppliers.services.suppliers_stock import SuppliersStockService


class SuppliersStockViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Stock.objects.none()
    permission_classes = [IsAdminUser]
    serializer_class = StockSerializer

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = SuppliersStockService()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_supplier_id(self):
        supplier_id = self.kwargs.get("supplier_pk")
        if not supplier_id:
            raise ValidationError({"supplier_pk": "This field is required."})
        return supplier_id

    @swagger_auto_schema(
        tags=["Suppliers Stock"],
        responses={200: StockSerializer(many=True)},
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        supplier_id = self.get_supplier_id()
        stock = self.service.get_active(supplier_id=supplier_id)
        serializer = self.get_serializer(stock, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Suppliers Stock"],
        request_body=StockSerializer,
        responses={201: StockSerializer},
    )
    def create(self, request: Request, **kwargs) -> Response:
        supplier_id = self.get_supplier_id()
        serializer = StockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        validated_data["supplier_id"] = supplier_id

        stock_item = self.service.create(serializer.validated_data)
        response_serializer = StockSerializer(stock_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Suppliers Stock"],
        responses={200: StockSerializer},
    )
    def retrieve(self, request: Request, pk: UUID, **kwarg) -> Response:
        supplier_id = self.get_supplier_id()
        stock_item = self.service.get_active_or_404(id=pk, supplier_id=supplier_id)
        serializer = self.get_serializer(stock_item)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Suppliers Stock"],
        request_body=StockSerializer,
        responses={204: "No Content"},
    )
    def partial_update(self, request: Request, pk: UUID, **kwargs) -> Response:
        serializer = StockSerializer(partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.update(serializer.validated_data, id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=["Suppliers Stock"],
        responses={204: "No Content"},
    )
    def destroy(self, request: Request, pk: UUID, **kwargs) -> Response:
        self.service.soft_delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
