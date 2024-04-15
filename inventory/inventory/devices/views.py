from django.http import FileResponse
import openpyxl

from django.conf import settings
import os

from django.shortcuts import get_object_or_404

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics as api_views
from rest_framework import status
from rest_framework.views import APIView

from inventory.business.models import Business

from inventory.core.view_mixins import IsBusinessOwner

from inventory.devices.models import Device
from inventory.devices.serializers import CSVUploadSerializer, DeviceSerializer
from inventory.devices.utils import create_devices_form_upload


class DeviceCreateAPIView(api_views.CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsBusinessOwner, IsAuthenticated]

    def perform_create(self, serializer):
        business_id = self.kwargs.get('business_id')
        serializer.save(business_id=business_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            "business_id": self.kwargs.get('business_id')
        })
        return context


class DeviceUpdateApiView(api_views.UpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsBusinessOwner, IsAuthenticated]


class DeviceDeleteApiView(api_views.DestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsBusinessOwner, IsAuthenticated]


class CSVUploadApiView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, business_id, *args, **kwargs):
        serializer = CSVUploadSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_file = serializer.validated_data['csv_file']
            wb = openpyxl.load_workbook(uploaded_file)
            sheet = wb.active
            business = get_object_or_404(Business, pk=business_id)

            results = create_devices_form_upload(sheet, business)

            return Response({'message': 'Devices imported successfully.', 'results': results},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def download_template(request):
    """
    Handles a request to download an Excel template file for device data entry.

    Returns:
        FileResponse: A response object that allows the file specified at the template_path to be downloaded by
        the client.
    """

    # Define the path to the template
    template_path = os.path.join(settings.BASE_DIR, 'staticfiles', 'template_file', 'template.xlsx')

    # Open the file for reading
    excel = open(template_path, 'rb')
    response = FileResponse(excel)

    # Content-type and prompt download
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response['Content-Disposition'] = 'attachment; filename=template.xlsx'
    return response
