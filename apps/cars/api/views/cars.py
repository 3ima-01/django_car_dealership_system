from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
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

from apps.cars.api.serializers.cars import (
    CarsSerializer,
)
from apps.cars.models import Cars
from apps.cars.services.cars import CarsService


class CarsViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Cars.objects.none()
    permission_classes = [IsAdminUser]
    serializer_class = CarsSerializer

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = CarsService()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

    @swagger_auto_schema(
        tags=["Cars"],
        responses={200: CarsSerializer(many=True)},
    )
    def list(self, request: Request) -> Response:
        cars = self.service.get_active()
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Cars"],
        request_body=CarsSerializer,
        responses={201: CarsSerializer},
    )
    def create(self, request: Request) -> Response:
        serializer = CarsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = self.service.create(serializer.validated_data)
        response_serializer = CarsSerializer(car)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Cars"],
        responses={200: CarsSerializer},
    )
    def retrieve(self, request: Request, pk: UUID) -> Response:
        car = self.service.get_active_or_404(id=pk)
        serializer = self.get_serializer(car)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Cars"],
        request_body=CarsSerializer,
        responses={204: "No Content"},
    )
    def partial_update(self, request: Request, pk: UUID) -> Response:
        serializer = CarsSerializer(partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.update(serializer.validated_data, id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(tags=["Cars"], responses={204: "No Content"})
    def destroy(self, request: Request, pk: UUID) -> Response:
        self.service.soft_delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
