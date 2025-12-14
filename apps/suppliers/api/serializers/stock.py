from rest_framework import serializers

from apps.suppliers.models.stock import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["id", "car", "supplier", "quantity", "price"]
        read_only_fields = ["id", "supplier"]
        ref_name = "SuppliersStock"
