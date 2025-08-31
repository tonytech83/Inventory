from rest_framework import serializers

from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ["business_name", "country", "is_visible", "owner"]
        extra_kwargs = {"owner": {"read_only": True}}
