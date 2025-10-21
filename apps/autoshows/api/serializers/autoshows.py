from rest_framework import serializers

from apps.autoshows.models import AutoShows


class AutoShowsPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoShows
        fields = ["id", "title", "location"]


class AutoShowsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoShows
        fields = ["title", "location", "car_preferences"]


class AutoShowsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoShows
        fields = ["title", "location", "car_preferences"]


class AutoShowsFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoShows
        fields = "__all__"
