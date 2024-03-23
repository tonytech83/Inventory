import json

from rest_framework import generics as api_views
from rest_framework.permissions import IsAuthenticated

from .serializers import SupplierSerializer

from django.views import generic as views

from inventory.suppliers.models import Supplier


class SupplierListView(views.ListView):
    model = Supplier
    template_name = 'suppliers/suppliers-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suppliers_list = []

        for supplier in self.get_queryset():
            supplier_dict = {
                "id": supplier.id,
                "name": supplier.name,
                "contact_name": supplier.contact_name,
                "phone_number": supplier.phone_number,
                "email": supplier.email,
            }

            suppliers_list.append(supplier_dict)

        # Convert the list of suppliers to JSON and add it to the context
        context['suppliers_json'] = json.dumps(suppliers_list)
        return context


class SupplierUpdateApiView(api_views.UpdateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierCreateApiView(api_views.CreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    # TODO: Check which other permissions classes I need
    permission_classes = [IsAuthenticated]


class SupplierDeleteApiView(api_views.DestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    # TODO: Check which other permissions classes I need
    permission_classes = [IsAuthenticated]
