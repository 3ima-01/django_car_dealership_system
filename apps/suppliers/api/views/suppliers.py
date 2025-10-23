from typing import Any
from uuid import UUID

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


class SuppliersAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = SuppliersService()

    def get(self, request: Request, id: UUID = None) -> Response:
        if id is not None:
            return self.get_by_id(request, id)

        suppliers = self.service.get_all_suppliers()
        serializer = SuppliersPublicSerializer(suppliers, many=True)
        return Response(serializer.data)

    def get_by_id(self, request: Request, id: UUID) -> Response:
        autoshow = self.service.get_supplier_by_id_or_404(id)
        serializer = SuppliersPublicSerializer(autoshow)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = SuppliersCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            autoshow = self.service.create_supplier(serializer.validated_data)
            response_serializer = SuppliersPublicSerializer(autoshow)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request: Request, id: UUID) -> Response:
        serializer = SuppliersUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            updated = self.service.update_supplier(id, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, id: UUID) -> Response:
        deleted = self.service.soft_delete_supplier(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
