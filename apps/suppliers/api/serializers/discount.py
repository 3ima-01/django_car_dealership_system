from rest_framework import serializers

from apps.suppliers.models.discount import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            "id",
            "name",
            "description",
            "discount_type",
            "value",
            "supplier",
            "cars",
            "autoshow",
            "start_date",
            "end_date",
        ]

        read_only_fields = ["id", "supplier"]
        ref_name = "SupplierDiscount"
