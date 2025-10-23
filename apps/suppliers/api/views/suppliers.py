from typing import Any
from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.suppliers.api.serializers.suppliers import (
    SuppliersCreateSerializer,
    SuppliersPublicSerializer,
    SuppliersUpdateSerializer,
)
from apps.suppliers.services.suppliers import SuppliersService


class SuppliersListView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = SuppliersService()

    @swagger_auto_schema(responses={200: SuppliersPublicSerializer(many=True)})
    def get(self, request: Request) -> Response:
        suppliers = self.service.get_all_suppliers()
        serializer = SuppliersPublicSerializer(suppliers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=SuppliersCreateSerializer, responses={201: SuppliersPublicSerializer})
    def post(self, request: Request) -> Response:
        serializer = SuppliersCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            autoshow = self.service.create_supplier(serializer.validated_data)
            response_serializer = SuppliersPublicSerializer(autoshow)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class SuppliersDetailView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = SuppliersService()

    @swagger_auto_schema(responses={200: SuppliersPublicSerializer})
    def get(self, request: Request, id: UUID) -> Response:
        autoshow = self.service.get_supplier_by_id_or_404(id)
        serializer = SuppliersPublicSerializer(autoshow)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=SuppliersUpdateSerializer, responses={204: "No Content"})
    def patch(self, request: Request, id: UUID) -> Response:
        serializer = SuppliersUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            updated = self.service.update_supplier(id, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={204: "No Content"})
    def delete(self, request: Request, id: UUID) -> Response:
        deleted = self.service.soft_delete_supplier(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
