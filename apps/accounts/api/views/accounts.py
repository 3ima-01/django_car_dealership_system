from typing import Any

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.accounts.api.serializers.accounts import (
    AccountsPublicSerializer,
    AccountsRegisterSerializer,
    VerifyEmailSerializer,
)
from apps.accounts.dtos.accounts import CustomerRegisterDTO
from apps.accounts.services.accounts import AccountsService


class AccountsViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = AccountsPublicSerializer

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = AccountsService()

    def get_queryset(self):
        from apps.accounts.models import Customers

        return Customers.objects.none()

    @swagger_auto_schema(
        tags=["Accounts"],
        request_body=AccountsRegisterSerializer,
        responses={201: AccountsPublicSerializer},
    )
    def create(self, request: Request):
        serializer = AccountsRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer_register_dto = CustomerRegisterDTO(**serializer.validated_data)
        customer = self.service.register(customer_register_dto)
        response_serializer = AccountsPublicSerializer(customer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Accounts"],
        manual_parameters=[
            openapi.Parameter(
                "token",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={204: "No Content"},
    )
    @action(detail=False, methods=["get"])
    def verify_email(self, request: Request):
        serializer = VerifyEmailSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        self.service.verify_email(serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)
