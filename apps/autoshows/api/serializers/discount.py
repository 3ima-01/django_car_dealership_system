from rest_framework import serializers

from apps.autoshows.models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ["id", "name", "description", "discount_type", "value", "autoshow", "cars", "start_date", "end_date"]
        read_only_fields = ["id", "autoshow"]
        ref_name = "AutoShowDiscount"
