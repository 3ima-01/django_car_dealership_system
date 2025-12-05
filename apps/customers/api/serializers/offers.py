from rest_framework import serializers

from apps.customers.models import Offers


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = ["id", "car", "max_price", "status"]
        read_only_fields = ["status"]
