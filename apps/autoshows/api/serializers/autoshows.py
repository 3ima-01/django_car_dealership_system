from rest_framework import serializers

from apps.autoshows.models import AutoShows


class AutoShowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoShows
        fields = "__all__"
