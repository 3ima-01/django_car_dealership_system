from rest_framework import serializers

from apps.autoshows.models import AutoShow


class AutoShowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoShow
        fields = ["id", "title", "location", "markup_percent", "balance", "car_preferences"]
        read_only_fields = ["id", "balance"]
