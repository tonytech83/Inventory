from django.urls import reverse_lazy
from django.views import generic as views

from inventory.suppliers.forms import CreateSupplierForm
from inventory.suppliers.models import Supplier


class SupplierListView(views.ListView):
    queryset = Supplier.objects.all()
    template_name = 'suppliers/suppliers-list.html'


class SupplierCreateView(views.CreateView):
    form_class = CreateSupplierForm
    template_name = 'suppliers/create-supplier.html'

    success_url = reverse_lazy('supplier-list')
