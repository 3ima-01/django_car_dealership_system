from typing import Any
from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.autoshows.api.serializers.autoshows import (
    AutoShowsCreateSerializer,
    AutoShowsPublicSerializer,
    AutoShowsUpdateSerializer,
)
from apps.autoshows.services.autoshows import AutoShowsService


class AutoShowsListView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = AutoShowsService()

    @swagger_auto_schema(responses={200: AutoShowsPublicSerializer(many=True)})
    def get(self, request: Request) -> Response:
        autoshows = self.service.get_all_autoshows()
        serializer = AutoShowsPublicSerializer(autoshows, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AutoShowsCreateSerializer, responses={201: AutoShowsPublicSerializer})
    def post(self, request: Request) -> Response:
        serializer = AutoShowsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        autoshow = self.service.create_autoshow(serializer.validated_data)
        response_serializer = AutoShowsPublicSerializer(autoshow)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class AutoShowsDetailView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = AutoShowsService()

    @swagger_auto_schema(responses={200: AutoShowsPublicSerializer})
    def get(self, request: Request, id: UUID) -> Response:
        autoshow = self.service.get_autoshow_by_id_or_404(id)
        serializer = AutoShowsPublicSerializer(autoshow)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AutoShowsUpdateSerializer, responses={204: "No Content"})
    def patch(self, request: Request, id: UUID) -> Response:
        serializer = AutoShowsUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.update_autoshow(id, serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={204: "No Content"})
    def delete(self, request: Request, id: UUID) -> Response:
        self.service.soft_delete_autoshow(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
