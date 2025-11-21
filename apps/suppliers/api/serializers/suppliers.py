from rest_framework import serializers

from apps.suppliers.models import Suppliers


class SuppliersPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = "__all__"


class SuppliersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ["title", "year", "country", "city"]


class SuppliersUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ["title", "year", "country", "city"]


class SuppliersFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = "__all__"
