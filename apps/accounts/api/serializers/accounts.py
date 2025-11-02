from rest_framework import serializers

from apps.accounts.models import Customers


class AccountsPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = "__all__"


class AccountsRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ["email", "password"]


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
