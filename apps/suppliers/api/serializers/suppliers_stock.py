from rest_framework import serializers

from apps.suppliers.models import SuppliersStock


class SuppliersStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliersStock
        fields = ["id", "car", "supplier", "quantity", "price"]
        read_only_fields = ["id"]
