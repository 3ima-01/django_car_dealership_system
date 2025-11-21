from rest_framework import serializers

from apps.accounts.models import Customers


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = Customers
        fields = ["email", "password", "first_name", "last_name"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class ChangeEmailSerializer(serializers.ModelSerializer):
    new_email = serializers.EmailField(source="email")

    class Meta:
        model = Customers
        fields = ["new_email"]


class ChangeEmailConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()


class ResetPasswordSerialiazer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)


class ResetPasswordConfirmSerialiazer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
