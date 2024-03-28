import random

from django.http import FileResponse
import openpyxl

from django.conf import settings
import os

from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics as api_views
from rest_framework import status
from rest_framework.views import APIView

from inventory.business.models import Business
from inventory.core.view_mixins import IsOwnerMixin, IsBusinessOwner

from inventory.devices.models import Device
from inventory.devices.serializers import CSVUploadSerializer, DeviceSerializer


class DeviceCreateAPIView( api_views.CreateAPIView):
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

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError as e:
            # Check for unique serial number
            if 'serial_number' in str(e):
                return Response({'detail': 'UNIQUE constraint failed: devices_device.serial_number'},
                                status=status.HTTP_400_BAD_REQUEST)
            # Check for 'device_name' uniqueness violation
            elif 'device_name' in str(e):

                return Response({'detail': 'The Device name is already used. Please use a unique Device name.'},
                                status=status.HTTP_400_BAD_REQUEST)
            # Generic integrity error
            else:
                return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_400_BAD_REQUEST)


class DeviceUpdateApiView(api_views.UpdateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsBusinessOwner, IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            # Call the superclass's update method to perform the actual update operation
            return super().update(request, *args, **kwargs)
        except IntegrityError as e:
            # Check for 'serial_number' uniqueness violation
            if 'serial_number' in str(e):
                return Response({'detail': 'UNIQUE constraint failed: devices_device.serial_number'},
                                status=status.HTTP_400_BAD_REQUEST)
            # Check for 'device_name' uniqueness violation
            elif 'device_name' in str(e):
                return Response({'detail': 'The Device name is already used. Please use a unique Device name.'},
                                status=status.HTTP_400_BAD_REQUEST)
            # Generic integrity error
            else:
                return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_400_BAD_REQUEST)


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

            results = []

            for row in sheet.iter_rows(min_row=3):  # Skip the first two header rows, thre
                # Random 4 digits if no serial number set
                four_random_digits = ''.join(str(random.randint(0, 9)) for _ in range(4))

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
                        serial_number=row[10].value if row[10].value else f'{row[0].value}-{four_random_digits}',
                        operating_system=row[11].value,
                        building=row[12].value,
                        owner_name=row[13].value,
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

    # Content-type and prompt download
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response['Content-Disposition'] = 'attachment; filename=template.xlsx'
    return response
