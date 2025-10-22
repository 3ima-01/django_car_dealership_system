from typing import Any
from uuid import UUID

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cars.api.exceptions import CarsValidationError
from apps.cars.api.serializers.cars import (
    CarsCreateSerializer,
    CarsPublicSerializer,
    CarsUpdateSerializer,
)
from apps.cars.services.cars import CarsService


class CarsAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = CarsService()

    def get(self, request: Request, id: UUID = None) -> Response:
        if id is not None:
            return self.get_by_id(request, id)

        cars = self.service.get_all_cars()
        serializer = CarsPublicSerializer(cars, many=True)
        return Response(serializer.data)

    def get_by_id(self, request: Request, id: UUID) -> Response:
        car = self.service.get_car_by_id_or_404(id)
        serializer = CarsPublicSerializer(car)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = CarsCreateSerializer(data=request.data)
        if serializer.is_valid():
            car = self.service.create_car(serializer.validated_data)
            response_serializer = CarsPublicSerializer(car)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        raise CarsValidationError

    def patch(self, request: Request, id: UUID) -> Response:
        serializer = CarsUpdateSerializer(data=request.data)
        if serializer.is_valid():
            updated = self.service.update_car(id, serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise CarsValidationError

    def delete(self, request: Request, id: UUID) -> Response:
        deleted = self.service.soft_delete_car(id)
        return Response(status=status.HTTP_204_NO_CONTENT)
