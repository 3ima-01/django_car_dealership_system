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

from apps.autoshows.api.serializers.autoshows import (
    AutoShowsCreateSerializer,
    AutoShowsPublicSerializer,
    AutoShowsUpdateSerializer,
)
from apps.autoshows.services.autoshows import AutoShowsService


class AutoShowsViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [AllowAny]
    serializer_class = AutoShowsPublicSerializer

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = AutoShowsService()

    def get_queryset(self):
        from apps.autoshows.models import AutoShows

        return AutoShows.objects.none()

    @swagger_auto_schema(
        tags=["AutoShows"],
        responses={200: AutoShowsPublicSerializer(many=True)},
    )
    def list(self, request: Request) -> Response:
        autoshows = self.service.get_all_autoshows()
        serializer = self.get_serializer(autoshows, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["AutoShows"],
        request_body=AutoShowsCreateSerializer,
        responses={201: AutoShowsPublicSerializer},
    )
    def create(self, request: Request) -> Response:
        serializer = AutoShowsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        autoshow = self.service.create_autoshow(serializer.validated_data)
        response_serializer = AutoShowsPublicSerializer(autoshow)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["AutoShows"],
        responses={200: AutoShowsPublicSerializer},
    )
    def retrieve(self, request: Request, pk: UUID) -> Response:
        autoshow = self.service.get_autoshow_by_id_or_404(pk)
        serializer = self.get_serializer(autoshow)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["AutoShows"],
        request_body=AutoShowsUpdateSerializer,
        responses={204: "No Content"},
    )
    def partial_update(self, request: Request, pk: UUID) -> Response:
        serializer = AutoShowsUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.update_autoshow(pk, serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=["AutoShows"],
        responses={204: "No Content"},
    )
    def destroy(self, request: Request, pk: UUID) -> Response:
        self.service.soft_delete_autoshow(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
