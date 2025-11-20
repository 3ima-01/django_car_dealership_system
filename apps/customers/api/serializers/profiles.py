from rest_framework import serializers

from apps.customers.models import Profiles


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = [
            "first_name",
            "last_name",
            "phone",
            "balance",
            "reserved_balance",
        ]
        read_only_fields = [
            "balance",
            "reserved_balance",
        ]
