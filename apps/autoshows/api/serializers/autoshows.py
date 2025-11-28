from rest_framework import serializers

from apps.autoshows.models import AutoShows


class AutoShowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoShows
        fields = ["id", "title", "location", "car_preferences", "markup_percent", "balance"]
        read_only_fields = ["id", "balance"]
