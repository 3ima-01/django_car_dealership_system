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

from apps.cars.api.serializers.cars import (
    CarsCreateSerializer,
    CarsPublicSerializer,
    CarsUpdateSerializer,
)
from apps.cars.models import Cars
from apps.cars.services.cars import CarsService


class CarsViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Cars.objects.none()
    permission_classes = [AllowAny]
    serializer_class = CarsPublicSerializer

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = CarsService()

    @swagger_auto_schema(
        tags=["Cars"],
        responses={200: CarsPublicSerializer(many=True)},
    )
    def list(self, request: Request) -> Response:
        cars = self.service.get_all_cars()
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Cars"],
        request_body=CarsCreateSerializer,
        responses={201: CarsPublicSerializer},
    )
    def create(self, request: Request) -> Response:
        serializer = CarsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = self.service.create_car(serializer.validated_data)
        response_serializer = CarsPublicSerializer(car)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Cars"],
        responses={200: CarsPublicSerializer},
    )
    def retrieve(self, request: Request, pk: UUID) -> Response:
        car = self.service.get_car_by_id_or_404(pk)
        serializer = self.get_serializer(car)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Cars"],
        request_body=CarsUpdateSerializer,
        responses={204: "No Content"},
    )
    def partial_update(self, request: Request, pk: UUID) -> Response:
        serializer = CarsUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.update_car(pk, serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=["Cars"],
        responses={204: "No Content"},
    )
    def destroy(self, request: Request, pk: UUID) -> Response:
        self.service.soft_delete_car(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
