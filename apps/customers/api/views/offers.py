from uuid import UUID

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.accounts.api.permisions import IsVerified
from apps.customers.api.serializers.offers import OfferSerializer
from apps.customers.services.offers import OffersService


class OffersViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = OfferSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = OffersService()

    def get_queryset(self):
        from apps.customers.models import Offers

        return Offers.objects.none()

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == "create":
            permissions.append(IsVerified())
        return permissions

    @swagger_auto_schema(
        tags=["Offers"],
        responses={200: OfferSerializer(many=True)},
    )
    def list(self, request: Request) -> Response:
        offers = self.service.my_offers(request.user)
        serializer = self.get_serializer(offers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Offers"],
        responses={201: OfferSerializer},
    )
    def create(
        self,
        request: Request,
    ):
        serializer = OfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["customer"] = request.user
        response = self.service.create_offer(**data)
        return Response(response, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Offers"],
        responses={200: OfferSerializer},
    )
    def retrieve(self, request: Request, pk: UUID) -> Response:
        offer = self.service.get_or_404(id=pk)
        serializer = self.get_serializer(offer)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["Offers"],
        responses={200: "Order successfully cancelled"},
    )
    @action(detail=True, methods=["post"], url_path="cancel", serializer_class=None)
    def cancel(self, request, pk: UUID):
        response = self.service.cancel_offer(
            offer_id=pk,
            customer=request.user,
        )
        return Response(response, status=status.HTTP_200_OK)
