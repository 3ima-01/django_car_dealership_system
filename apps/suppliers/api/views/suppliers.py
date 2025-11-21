from typing import Any
from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.suppliers.api.serializers.suppliers import (
    SuppliersCreateSerializer,
    SuppliersPublicSerializer,
    SuppliersUpdateSerializer,
)
from apps.suppliers.services.suppliers import SuppliersService


class SuppliersViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [AllowAny]
    serializer_class = SuppliersPublicSerializer

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = SuppliersService()

    def get_queryset(self):
        from apps.suppliers.models import Suppliers

        return Suppliers.objects.none()

    @swagger_auto_schema(
        tags=["Suppliers"],
        responses={200: SuppliersPublicSerializer(many=True)},
    )
    def list(self, request: Request) -> Response:
        suppliers = self.service.get_all_suppliers()
        serializer = self.get_serializer(suppliers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Suppliers"],
        request_body=SuppliersCreateSerializer,
        responses={201: SuppliersPublicSerializer},
    )
    def create(self, request: Request) -> Response:
        serializer = SuppliersCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        supplier = self.service.create_supplier(serializer.validated_data)
        response_serializer = SuppliersPublicSerializer(supplier)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Suppliers"],
        responses={200: SuppliersPublicSerializer},
    )
    def retrieve(self, request: Request, pk: UUID) -> Response:
        supplier = self.service.get_supplier_by_id_or_404(pk)
        serializer = self.get_serializer(supplier)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Suppliers"],
        request_body=SuppliersUpdateSerializer,
        responses={204: "No Content"},
    )
    def partial_update(self, request: Request, pk: UUID) -> Response:
        serializer = SuppliersUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.update_supplier(pk, serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=["Suppliers"],
        responses={204: "No Content"},
    )
    def destroy(self, request: Request, pk: UUID) -> Response:
        self.service.soft_delete_supplier(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
