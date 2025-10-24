from typing import Any
from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cars.api.serializers.cars import (
    CarsCreateSerializer,
    CarsPublicSerializer,
    CarsUpdateSerializer,
)
from apps.cars.services.cars import CarsService


class CarsListView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = CarsService()

    @swagger_auto_schema(responses={200: CarsPublicSerializer(many=True)})
    def get(self, request: Request) -> Response:
        cars = self.service.get_all_cars()
        serializer = CarsPublicSerializer(cars, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CarsCreateSerializer, responses={201: CarsPublicSerializer})
    def post(self, request: Request) -> Response:
        serializer = CarsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = self.service.create_car(serializer.validated_data)
        response_serializer = CarsPublicSerializer(car)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CarsDetailView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = CarsService()

    @swagger_auto_schema(responses={200: CarsPublicSerializer})
    def get(self, request: Request, id: UUID) -> Response:
        car = self.service.get_car_by_id_or_404(id)
        serializer = CarsPublicSerializer(car)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CarsUpdateSerializer, responses={204: "No Content"})
    def patch(self, request: Request, id: UUID) -> Response:
        serializer = CarsUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.update_car(id, serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={204: "No Content"})
    def delete(self, request: Request, id: UUID) -> Response:
        self.service.soft_delete_car(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
