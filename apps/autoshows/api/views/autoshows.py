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

from apps.autoshows.api.serializers.autoshows import AutoShowsSerializer
from apps.autoshows.models import AutoShows
from apps.autoshows.services.autoshows import AutoShowsService


class AutoShowsViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = AutoShows.objects.none()
    permission_classes = [AllowAny]
    serializer_class = AutoShowsSerializer

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = AutoShowsService()

    @swagger_auto_schema(
        tags=["AutoShows"],
        responses={200: AutoShowsSerializer(many=True)},
    )
    def list(self, request: Request) -> Response:
        autoshows = self.service.get_all()
        serializer = self.get_serializer(autoshows, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["AutoShows"],
        request_body=AutoShowsSerializer,
        responses={201: AutoShowsSerializer},
    )
    def create(self, request: Request) -> Response:
        serializer = AutoShowsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        autoshow = self.service.create(serializer.validated_data)
        response_serializer = AutoShowsSerializer(autoshow)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        tags=["AutoShows"],
        responses={200: AutoShowsSerializer},
    )
    def retrieve(self, request: Request, pk: UUID) -> Response:
        autoshow = self.service.get_by_filter_or_404(id=pk)
        serializer = self.get_serializer(autoshow)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["AutoShows"],
        request_body=AutoShowsSerializer,
        responses={202: AutoShowsSerializer},
    )
    def partial_update(self, request: Request, pk: UUID) -> Response:
        serializer = AutoShowsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        autoshow = self.service.update(pk, serializer.validated_data)
        response_serializer = AutoShowsSerializer(autoshow)
        return Response(
            response_serializer.data,
            status=status.HTTP_202_ACCEPTED,
        )

    @swagger_auto_schema(
        tags=["AutoShows"],
        responses={204: "No Content"},
    )
    def destroy(self, request: Request, pk: UUID) -> Response:
        self.service.soft_delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
