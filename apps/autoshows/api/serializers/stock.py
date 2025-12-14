from rest_framework import serializers

from apps.autoshows.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id", "car", "autoshow", "quantity", "price"]
        read_only_field = ["id"]
        ref_name = "AutoShowsStock"
