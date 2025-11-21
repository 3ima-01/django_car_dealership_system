from rest_framework import serializers

from apps.autoshows.models import AutoShowsStock


class AutoShowsStockPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoShowsStock
        fields = "__all__"
