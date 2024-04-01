import json

from rest_framework import generics as api_views
from rest_framework.permissions import IsAuthenticated

from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.db import IntegrityError

from inventory.business.models import Business
from inventory.business.serializers import BusinessSerializer
from inventory.business.utils import prepare_device_list, filter_devices_queryset
from inventory.core.utils import catches_exception
from inventory.organization.models import Organization
from inventory.suppliers.models import Supplier


class BusinessView(auth_mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'business/business.html'

    def get_queryset(self):
        return (Business.objects.all()
                .prefetch_related('device_set', ))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = context['object']

        device_queryset = filter_devices_queryset(self, business)
        device_list = prepare_device_list(device_queryset)

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

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError as e:
            catches_exception(e)


class UpdateBusinessApiView(api_views.UpdateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError as e:
            catches_exception(e)
