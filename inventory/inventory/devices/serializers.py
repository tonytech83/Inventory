from rest_framework import serializers

from inventory.devices.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

    def create(self, validated_data):
        device = Device.objects.create(**validated_data)

        return device


class CSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def create(self, validated_data):
        return validated_data
