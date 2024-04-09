import json

from rest_framework import generics as api_views
from rest_framework.permissions import IsAuthenticated

from .serializers import SupplierSerializer

from django.views import generic as views
from django.contrib.auth.mixins import LoginRequiredMixin

from inventory.suppliers.models import Supplier
from .utils import prepare_suppliers_list


class SupplierListView(LoginRequiredMixin, views.ListView):
    model = Supplier
    template_name = 'suppliers/suppliers-list.html'

    @property
    def supplier_name_pattern(self):
        return self.request.GET.get('supplier_name_pattern')

    def get_queryset(self):
        queryset = super().get_queryset()
        supplier_name_pattern = self.supplier_name_pattern

        if supplier_name_pattern:
            queryset = queryset.filter(name__icontains=self.supplier_name_pattern)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier_name_pattern'] = self.supplier_name_pattern or ''
        suppliers_list = prepare_suppliers_list(self.get_queryset())

        # Convert the list of suppliers to JSON and add it to the context
        context['suppliers_json'] = json.dumps(suppliers_list)
        context['suppliers_exists'] = Supplier.objects.exists()
        return context


class SupplierUpdateApiView(LoginRequiredMixin, api_views.UpdateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierCreateApiView(api_views.CreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]


class SupplierDeleteApiView(api_views.DestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
