from rest_framework import serializers

from apps.autoshows.models import AutoShowsStock


class AutoShowsStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoShowsStock
        fields = ["id", "car", "autoshow", "quantity", "price"]
        read_only_field = ["id"]
