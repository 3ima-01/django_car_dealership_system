from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.accounts.api.serializers.accounts import (
    ChangeEmailConfirmSerializer,
    ChangeEmailSerializer,
    ChangePasswordSerializer,
    RegisterSerializer,
    ResetPasswordConfirmSerialiazer,
    ResetPasswordSerialiazer,
    VerifyEmailSerializer,
)
from apps.accounts.services.accounts import AccountsService


class AccountsViewSet(CreateModelMixin, viewsets.ViewSet):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.service = AccountsService()

    @swagger_auto_schema(
        tags=["Accounts"],
        request_body=RegisterSerializer,
    )
    def create(self, request: Request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.service.register(**serializer.validated_data)
        return Response(response, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["Accounts"], request_body=ResetPasswordSerialiazer)
    @action(
        detail=False,
        methods=["post"],
        url_path="reset-password",
    )
    def reset_password(self, request: Request):
        serializer = ResetPasswordSerialiazer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.service.reset_password(**serializer.validated_data)
        return Response(response, status=status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(tags=["Accounts"], request_body=ResetPasswordConfirmSerialiazer)
    @action(
        detail=False,
        methods=["post"],
        url_path="reset-password/confirm",
    )
    def reset_password_confirm(self, request: Request):
        serializer = ResetPasswordConfirmSerialiazer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.service.reset_password_confirm(**serializer.validated_data)
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Accounts"], request_body=ChangePasswordSerializer)
    @action(
        detail=False,
        methods=["patch"],
        url_path="change-password",
        permission_classes=[IsAuthenticated],
    )
    def change_password(self, request: Request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.service.change_password(request.user, **serializer.validated_data)
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Accounts"], request_body=ChangeEmailSerializer)
    @action(
        detail=False,
        methods=["patch"],
        url_path="change-email",
        permission_classes=[IsAuthenticated],
    )
    def change_email(self, request: Request):
        serializer = ChangeEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.service.change_email(request.user, serializer.validated_data["email"])
        return Response(response, status=status.HTTP_202_ACCEPTED)

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
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="change-email/confirm",
    )
    def change_email_confirm(self, request: Request):
        serializer = ChangeEmailConfirmSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        response = self.service.change_email_confirm(**serializer.validated_data)
        return Response(response, status=status.HTTP_200_OK)

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
    @action(
        detail=False,
        methods=["get"],
    )
    def verification(self, request: Request):
        serializer = VerifyEmailSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        self.service.verify_email(**serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)
