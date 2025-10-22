from rest_framework import serializers

from apps.cars.models import Cars


class CarsPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = ["id", "year", "brand", "model", "color", "body_type", "engine_type", "horse_power", "properties"]


class CarsCreateSerializer(serializers.ModelSerializer):
    engine_type = serializers.ChoiceField(choices=Cars.ENGINE_TYPES)

    class Meta:
        model = Cars
        fields = ["year", "brand", "model", "color", "body_type", "engine_type", "horse_power", "properties"]


class CarsUpdateSerializer(serializers.ModelSerializer):
    engine_type = serializers.ChoiceField(choices=Cars.ENGINE_TYPES)

    class Meta:
        model = Cars
        fields = ["year", "brand", "model", "color", "body_type", "engine_type", "horse_power", "properties"]


class CarsFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = "__all__"
