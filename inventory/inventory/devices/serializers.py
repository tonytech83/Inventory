from rest_framework import serializers


class CSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()

    def create(self, validated_data):
        # Handle file processing here if necessary
        return validated_data
