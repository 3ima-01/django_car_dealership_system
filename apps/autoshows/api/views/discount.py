from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.autoshows.api.serializers.discount import DiscountSerializer
from apps.autoshows.models import Discount
from apps.autoshows.services.discount import DiscountService


class DiscountViewSet(
    ListModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = Discount.objects.none()
    permission_classes = [IsAdminUser]
    serializer_class = DiscountSerializer

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = DiscountService()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

    @swagger_auto_schema(
        tags=["AutoShows Discount"],
        responses={200: DiscountSerializer(many=True)},
    )
    def list(self, request: Request, **kwarg) -> Response:
        autoshow_id = self.kwargs.get("autoshow_pk")
        if not autoshow_id:
            raise ValidationError("pk is required")
        discounts = self.service.get_active(autoshow_id=autoshow_id)
        serializer = self.get_serializer(discounts, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["AutoShows Discount"],
        request_body=DiscountSerializer,
        responses={201: DiscountSerializer},
    )
    def create(self, request: Request, **kwarg) -> Response:
        autoshow_id = self.kwargs.get("autoshow_pk")
        if not autoshow_id:
            raise ValidationError("pk is required")
        serializer = DiscountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        autoshow = self.service.create(autoshow_id, serializer.validated_data)
        response_serializer = DiscountSerializer(autoshow)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["AutoShows Discount"],
        responses={200: DiscountSerializer},
    )
    def retrieve(self, request: Request, pk: UUID, **kwarg) -> Response:
        autoshow_id = self.kwargs.get("autoshow_pk")
        if not autoshow_id:
            raise ValidationError("pk is required")
        autoshow = self.service.get_active_or_404(id=pk)
        serializer = self.get_serializer(autoshow)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["AutoShows Discount"],
        request_body=DiscountSerializer,
        responses={204: "No Content"},
    )
    def partial_update(self, request: Request, pk: UUID, **kwargs) -> Response:
        autoshow_id = self.kwargs.get("autoshow_pk")
        if not autoshow_id:
            raise ValidationError("pk is required")
        serializer = DiscountSerializer(partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.update(serializer.validated_data, id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=["AutoShows Discount"],
        responses={204: "No Content"},
    )
    def destroy(self, request: Request, pk: UUID, **kwargs) -> Response:
        autoshow_id = self.kwargs.get("autoshow_pk")
        if not autoshow_id:
            raise ValidationError("pk is required")
        self.service.soft_delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
