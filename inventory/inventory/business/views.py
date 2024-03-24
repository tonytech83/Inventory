import json
from datetime import timedelta

from django.shortcuts import get_list_or_404
from rest_framework import generics as api_views

from django.utils.timezone import now

from django.urls import reverse
from django.views import generic as views
from rest_framework.permissions import IsAuthenticated

from inventory.business.forms import EditBusinessForm
from inventory.business.models import Business
from inventory.business.serializers import BusinessSerializer
from inventory.suppliers.models import Supplier


class BusinessView(views.DetailView):
    template_name = 'business/business.html'

    def get_queryset(self):
        return Business.objects.all().prefetch_related(
            'device_set',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = context['object']

        # TODO: to made mixin for queries below
        # Support
        no_support = self.request.GET.get('no_support', None)
        no_reviewed = self.request.GET.get('no_reviewed', None)

        # Status
        in_operation = self.request.GET.get('in_operation', None)
        is_decommissioned = self.request.GET.get('is_decommissioned', None)
        is_pending_setup = self.request.GET.get('is_pending_setup', None)
        is_offline = self.request.GET.get('is_offline', None)
        not_defined = self.request.GET.get('not_defined', None)
        is_exception = self.request.GET.get('is_exception', None)

        device_queryset = business.device_set.all()

        if no_support == 'true':
            device_queryset = device_queryset.filter(eos__lt=now().date())

        if no_reviewed == 'true':
            one_year_ago = now() - timedelta(days=365)
            device_queryset = device_queryset.filter(updated_at__lte=one_year_ago)

        if in_operation == 'true':
            device_queryset = device_queryset.filter(status='In operation')

        if is_decommissioned == 'true':
            device_queryset = device_queryset.filter(status='Decommissioned')

        if is_pending_setup == 'true':
            device_queryset = device_queryset.filter(status='Pending Setup')

        if is_offline == 'true':
            device_queryset = device_queryset.filter(status='Offline')

        if not_defined == 'true':
            device_queryset = device_queryset.filter(status='Not defined yet')

        if is_exception == 'true':
            device_queryset = device_queryset.filter(status='Exception')

        device_list = []

        for device in device_queryset:
            device_dict = {
                'id': device.id,
                'device_name': device.device_name,
                'domain': device.domain,
                'description': device.description,
                'status': device.status,
                'manufacturer': device.manufacturer,
                'model': device.model,
                'ip_address': device.ip_address,
                'ip_address_sec': device.ip_address_sec,
                'operating_system': device.operating_system,
                'building': device.building,
                'category': device.category,
                'sub_category': device.sub_category,
                'serial_number': device.serial_number,
                'owner_name': device.owner_name,
                # Support
                'support_model': device.support_model,
                'purchase_order_number': device.purchase_order_number,
                'invoice_img': str(device.invoice_img),
                'sos': str(device.sos),
                'eos': str(device.eos),
                'eol': str(device.eol),
                # Risk
                'business_processes_at_risk': device.business_processes_at_risk,
                'impact': device.impact,
                'likelihood': device.likelihood,
                # Supplier
                'supplier_name': device.supplier_display,
            }

            device_list.append(device_dict)

        suppliers = get_list_or_404(Supplier)
        suppliers_list = [{
            "id": supplier.id,
            "name": supplier.name,
            "contact_name": supplier.contact_name,
            "phone_number": supplier.phone_number,
            "email": supplier.email,
        } for supplier in suppliers]

        # Convert the list of suppliers to JSON and add it to the context
        context['suppliers_json'] = json.dumps(suppliers_list)
        context['devices_json'] = json.dumps(device_list)

        return context


class CreateBusinessApiView(api_views.CreateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UpdateBusinessApiView(api_views.UpdateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

# class EditBusinessView(views.UpdateView):
#     queryset = Business.objects.all()
#     form_class = EditBusinessForm
#     template_name = 'business/edit-business.html'
#
#     def get_success_url(self):
#         """
#         Returns the URL to redirect to after processing a valid form.
#         """
#         return reverse('business', kwargs={'pk': self.object.pk})
