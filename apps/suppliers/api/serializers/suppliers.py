from rest_framework import serializers

from apps.suppliers.models import Suppliers


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ["id", "title", "year", "country", "city"]
        read_only_fields = ["id"]
