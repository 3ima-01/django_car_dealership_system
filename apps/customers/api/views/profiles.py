from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.customers.api.serializers.profiles import ProfileSerializer


class ProfileViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    @swagger_auto_schema(
        tags=["Profiles"],
        responses={200: ProfileSerializer},
    )
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request: Request):
        profile = request.user.profile
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
