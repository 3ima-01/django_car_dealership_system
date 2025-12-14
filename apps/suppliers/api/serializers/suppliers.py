from rest_framework import serializers

from apps.suppliers.models.supplier import Supplier


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "title", "year", "country", "city"]
        read_only_fields = ["id"]
