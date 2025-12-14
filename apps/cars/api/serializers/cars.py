from rest_framework import serializers

from apps.cars.models import Cars


class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = ["id", "year", "brand", "model", "color", "body_type", "engine_type", "horse_power", "properties"]
        read_only_fields = ["id"]
