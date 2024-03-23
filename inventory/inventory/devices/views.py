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


# class DeviceCreateView(views.CreateView):
#     model = Device
#     form_class = DeviceCreateForm
#     template_name = 'devices/create-device.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['business_id'] = self.kwargs.get('business_id')
#
#         if 'risk_form' not in context:
#             context['risk_form'] = RiskForm(self.request.POST or None, prefix='risk')
#         if 'support_form' not in context:
#             context['support_form'] = SupportForm(self.request.POST or None, prefix='support')
#
#         return context
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         risk_form = context['risk_form']
#         support_form = context['support_form']
#
#         with transaction.atomic():
#             """
#             Use Django's transaction.atomic decorator to ensure that the entire operation is atomic.
#             This means either all operations succeed, or none do, preventing database integrity errors.
#             Additionally, save the Device instance only after the Risk and Support instances have been saved
#             and associated with it.
#             """
#             if form.is_valid() and risk_form.is_valid() and support_form.is_valid():
#                 # Temporarily save the Device form without committing to the DB
#                 self.object = form.save(commit=False)
#                 # Save the Risk and Support forms and associate them with the Device
#                 risk = risk_form.save()
#                 support = support_form.save()
#                 self.object.risk = risk
#                 self.object.support = support
#
#                 # Capture the business_id from URL parameters and associate it with the device
#                 business_id = self.kwargs.get('business_id')
#                 business = get_object_or_404(Business, pk=business_id)
#                 self.object.business = business
#
#                 # Now save the Device object to the database
#                 self.object.save()
#
#                 return redirect(self.get_success_url())
#             else:
#                 # If forms are not valid, return to the form with errors
#                 return self.form_invalid(form)
#
#     def get_success_url(self):
#         # Redirect to the business detail page
#         return reverse_lazy('business', kwargs={'pk': self.kwargs.get('business_id')})

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


# TODO: Check for login permissions
# class DeviceEditView(views.UpdateView):
#     queryset = (Device.objects.all()
#                 .prefetch_related('support')
#                 .prefetch_related('risk'))
#
#     form_class = DeviceEditForm
#     template_name = 'devices/edit-device.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if 'support_form' not in context:
#             context['support_form'] = SupportForm(instance=self.object.support)
#         if 'risk_form' not in context:
#             context['risk_form'] = RiskForm(instance=self.object.risk)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         support_form = SupportForm(request.POST, instance=self.object.support)
#         risk_form = RiskForm(request.POST, instance=self.object.risk)
#
#         if form.is_valid() and support_form.is_valid() and risk_form.is_valid():
#             return self.form_valid(form, support_form, risk_form)
#         else:
#             return self.form_invalid(form, support_form, risk_form)
#
#     def form_valid(self, form, support_form, risk_form):
#         self.object = form.save()
#         support_form.save()
#         risk_form.save()
#         return redirect(self.get_success_url())
#
#     def form_invalid(self, form, support_form, risk_form):
#         return self.render_to_response(
#             self.get_context_data(form=form, support_form=support_form, risk_form=risk_form))
#
#     def get_success_url(self):
#         # Redirect to the business detail page
#         return reverse_lazy('business', kwargs={'pk': self.object.business_id})


# class DeviceDeleteView(views.DeleteView):
#     queryset = Device.objects.all()
#     form_class = DeviceDeleteForm
#     template_name = 'devices/delete-device.html'
#
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['instance'] = self.object
#
#         return kwargs
#
#     def get_success_url(self):
#         # Redirect to the business detail page
#         return reverse_lazy('business', kwargs={'pk': self.object.business_id})


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
            # return Response({'message': 'Devices imported successfully.'}, status=status.HTTP_200_OK)
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
