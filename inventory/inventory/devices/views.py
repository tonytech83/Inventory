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

from inventory.devices.models import Device
from inventory.devices.serializers import CSVUploadSerializer, DeviceSerializer


class DeviceCreateAPIView(api_views.CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    # TODO: Check which other permissions classes I need

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
    # TODO: Check which other permissions classes I need


class DeviceDeleteApiView(api_views.DestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    # TODO: Check which other permissions classes I need
    permission_classes = [IsAuthenticated]


class CSVUploadApiView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, business_id, *args, **kwargs):
        serializer = CSVUploadSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_file = serializer.validated_data['csv_file']
            wb = openpyxl.load_workbook(uploaded_file)
            sheet = wb.active
            business = get_object_or_404(Business, pk=business_id)

            results = []

            for row in sheet.iter_rows(min_row=3):  # Skip the first two header rows
                try:
                    Device.objects.create(
                        device_name=row[0].value,
                        domain=row[1].value,
                        description=row[2].value,
                        status=row[3].value,
                        category=row[4].value,
                        sub_category=row[5].value,
                        manufacturer=row[6].value,
                        model=row[7].value,
                        ip_address=row[8].value,
                        ip_address_sec=row[9].value,
                        serial_number=row[10].value,
                        operating_system=row[11].value,
                        building=row[12].value,
                        owner_name=row[13].value,
                        # TODO: Fix support and risk, no models anymore
                        # support=support,
                        # risk=risk,
                        business=business,
                    )
                    results.append({'device_name': row[0].value, 'status': 'success'})
                except Exception as e:
                    results.append({'device_name': row[0].value, 'status': 'Error', 'error': str(e)})
                    continue

            return Response({'message': 'Devices imported successfully.', 'results': results},
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def download_template(request):
    # Define the path to the template
    template_path = os.path.join(settings.BASE_DIR, 'staticfiles', 'template_file', 'template.xlsx')

    # Open the file for reading
    excel = open(template_path, 'rb')
    response = FileResponse(excel)

    # Set the content-type and disposition to prompt download
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response['Content-Disposition'] = 'attachment; filename=template.xlsx'
    return response
