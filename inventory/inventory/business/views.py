import json
from datetime import timedelta

from django.db.models import ExpressionWrapper, F, fields

from rest_framework import generics as api_views

from django.utils.timezone import now

from django.views import generic as views
from rest_framework.permissions import IsAuthenticated

from inventory.business.models import Business
from inventory.business.serializers import BusinessSerializer
from inventory.organization.models import Organization

from inventory.suppliers.models import Supplier


class BusinessView(views.DetailView):
    template_name = 'business/business.html'

    def get_queryset(self):
        return (Business.objects.all()
                .prefetch_related('device_set', ))

    def get_devices_queryset(self, business):
        device_queryset = business.device_set.all()
        filters = self.request.GET

        # Periods
        today = now().date()
        one_year_ago = now() - timedelta(days=365)
        six_months_ahead = now() + timedelta(days=182)
        one_year_ahead = now() + timedelta(days=365)
        one_year_from_now = today + timedelta(days=365)
        six_months_from_now = today + timedelta(days=182)
        three_months_from_now = today + timedelta(days=90)

        # Status Filters
        if 'in_operation' in filters:
            device_queryset = device_queryset.filter(status='In operation')
        if 'is_decommissioned' in filters:
            device_queryset = device_queryset.filter(status='Decommissioned')
        if 'is_pending_setup' in filters:
            device_queryset = device_queryset.filter(status='Pending Setup')
        if 'is_offline' in filters:
            device_queryset = device_queryset.filter(status='Offline')
        if 'not_defined' in filters:
            device_queryset = device_queryset.filter(status='Not defined yet')
        if 'is_exception' in filters:
            device_queryset = device_queryset.filter(status='Exception')

        # Not Reviewed Filter
        if 'no_reviewed' in filters:
            device_queryset = device_queryset.filter(updated_at__lte=one_year_ago)

        # Support Filters
        if 'no_support' in filters:
            device_queryset = device_queryset.filter(eos__lt=now().date())

        if 'lt_three_months_and_no_support' in filters:
            device_queryset = device_queryset.filter(eos__range=(today, three_months_from_now))

        if 'lt_six_gt_three_months' in filters:
            device_queryset = device_queryset.filter(eos__range=(three_months_from_now, six_months_from_now))

        if 'lt_year_gt_six_month' in filters:
            device_queryset = device_queryset.filter(eos__range=(six_months_ahead, one_year_ahead))

        if 'count_devices_in_support' in filters:
            device_queryset = device_queryset.filter(eos__gt=one_year_from_now)

        if 'count_devices_unknown_support' in filters:
            device_queryset = device_queryset.filter(eos=None)

        # Risk Filters
        if 'risk_below_five' in filters:
            device_queryset = device_queryset.annotate(
                calculated_risk_score=ExpressionWrapper(
                    F('impact') * F('likelihood'),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_risk_score__lt=5)

        if 'between_five_and_ten' in filters:
            device_queryset = device_queryset.annotate(
                calculated_risk_score=ExpressionWrapper(
                    F('impact') * F('likelihood'),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_risk_score__gte=5, calculated_risk_score__lte=10)

        if 'above_ten' in filters:
            device_queryset = device_queryset.annotate(
                calculated_risk_score=ExpressionWrapper(
                    F('impact') * F('likelihood'),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_risk_score__gt=10)

        return device_queryset

    @staticmethod
    def prepare_device_list(device_queryset):
        """
        Receive a QuerySet and return it into list of dictionaries
        """
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
                # Support fields
                'support_model': device.support_model,
                'purchase_order_number': device.purchase_order_number,
                'invoice_img': device.invoice_img.url if device.invoice_img else None,
                'sos': device.sos.isoformat() if device.sos else None,
                'eos': device.eos.isoformat() if device.eos else None,
                'eol': device.eol.isoformat() if device.eol else None,
                # Risk fields
                'business_processes_at_risk': device.business_processes_at_risk,
                'impact': device.impact,
                'likelihood': device.likelihood,
                # Supplier
                'supplier_name': device.supplier_display,
            }
            device_list.append(device_dict)

        return device_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = context['object']

        device_queryset = self.get_devices_queryset(business)
        device_list = self.prepare_device_list(device_queryset)

        # suppliers = get_list_or_404(Supplier)
        suppliers = Supplier.objects.all()
        suppliers_list = [{
            "id": supplier.id,
            "name": supplier.name,
            "contact_name": supplier.contact_name,
            "phone_number": supplier.phone_number,
            "email": supplier.email,
        } for supplier in suppliers]

        context['has_devices'] = device_queryset.exists()
        context['suppliers_json'] = json.dumps(suppliers_list)
        context['devices_json'] = json.dumps(device_list)
        return context


class CreateBusinessApiView(api_views.CreateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, organization=Organization.objects.first())


class UpdateBusinessApiView(api_views.UpdateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
