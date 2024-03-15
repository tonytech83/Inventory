import json
from django.urls import reverse

from django.core.serializers import serialize
from django.urls import reverse_lazy
from django.views import generic as views

from inventory.suppliers.forms import CreateSupplierForm, EditSupplierForm, DeviceSupplierForm
from inventory.suppliers.models import Supplier


class SupplierListView(views.ListView):
    model = Supplier
    template_name = 'suppliers/suppliers-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suppliers_list = []

        for supplier in self.get_queryset():
            supplier_dict = {
                "edit_url": reverse('edit-supplier', kwargs={'pk': supplier.pk}),  # Generate edit URL
                "name": supplier.name,
                "contact_name": supplier.contact_name,
                "phone_number": supplier.phone_number,
                "email": supplier.email,
            }

            suppliers_list.append(supplier_dict)

        # Convert the list of suppliers to JSON and add it to the context
        context['suppliers_json'] = json.dumps(suppliers_list)
        return context


class SupplierCreateView(views.CreateView):
    form_class = CreateSupplierForm
    template_name = 'suppliers/create-supplier.html'

    success_url = reverse_lazy('supplier-list')


class SupplierEditView(views.UpdateView):
    queryset = Supplier.objects.all()
    form_class = EditSupplierForm
    template_name = 'suppliers/edit-supplier.html'

    success_url = reverse_lazy('supplier-list')


class SupplierDeleteView(views.DeleteView):
    queryset = Supplier.objects.all()
    form_class = DeviceSupplierForm
    template_name = 'suppliers/delete-supplier.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object

        return kwargs

    def get_success_url(self):
        return reverse_lazy('supplier-list')
