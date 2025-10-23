from typing import Any
from uuid import UUID

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


class AutoShowsAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = AutoShowsService()

    def get(self, request: Request, id: UUID = None) -> Response:
        if id is not None:
            return self.get_by_id(request, id)

        autoshows = self.service.get_all_autoshows()
        serializer = AutoShowsPublicSerializer(autoshows, many=True)
        return Response(serializer.data)

    def get_by_id(self, request: Request, id: UUID) -> Response:
        autoshow = self.service.get_autoshow_by_id_or_404(id)
        serializer = AutoShowsPublicSerializer(autoshow)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = AutoShowsCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            autoshow = self.service.create_autoshow(serializer.validated_data)
            response_serializer = AutoShowsPublicSerializer(autoshow)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request: Request, id: UUID) -> Response:
        serializer = AutoShowsUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            updated = self.service.update_autoshow(id, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, id: UUID) -> Response:
        deleted = self.service.soft_delete_autoshow(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
