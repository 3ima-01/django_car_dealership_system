from typing import Any

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.autoshows.api.serializers.autoshows import AutoShowsSerializer
from apps.autoshows.models import AutoShows
from apps.autoshows.services.autoshows import AutoShowsService


class AutoShowsAPIView(APIView):
    queryset = AutoShows.objects.all()
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = AutoShowsService()

    def get(self, request, pk=None):
        if pk:
            return self.get_by_id(request, pk)

        autoshows = self.service.get_all_autoshows()
        serializer = AutoShowsSerializer(autoshows, many=True)
        return Response(serializer.data)

    def get_by_id(self, request, pk):
        autoshow = self.service.get_autoshow_by_id_or_none(pk)
        serializer = AutoShowsSerializer(autoshow)
        return Response(serializer.data)

    def post(self, request):
        serializer = AutoShowsSerializer(data=request.data)
        if serializer.is_valid():
            autoshow = self.service.create_autoshow(serializer.validated_data)
            response_serializer = AutoShowsSerializer(autoshow)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
