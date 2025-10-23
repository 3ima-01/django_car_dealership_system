from rest_framework import serializers

from apps.suppliers.models import SuppliersStock


class SuppliersStockPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliersStock
        fields = "__all__"


class SuppliersStockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliersStock
        fields = ["car_id", "supplier_id", "quantity", "price"]


class SuppliersStockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliersStock
        fields = ["quantity", "price"]


class SuppliersStockFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliersStock
        fields = "__all__"
