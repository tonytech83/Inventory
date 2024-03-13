import json

from django.urls import reverse_lazy, reverse
from django.views import generic as views

from inventory.business.forms import CreateBusinessForm, EditBusinessForm
from inventory.business.models import Business


class BusinessView(views.DetailView):
    queryset = Business.objects.all().prefetch_related(
        'device_set',
        'device_set__support',
        'device_set__risk',
    )

    template_name = 'business/business.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the business from context
        business = context['business']
        device_list = []

        for device in business.device_set.all():
            device_dict = {
                'edit_url': reverse('edit-device', kwargs={'pk': device.pk}),  # Generate edit URL
                'device_name': device.device_name,
                'status': device.status,
                'manufacturer': device.manufacturer,
                'model': device.model,
                'category': device.category,
                'sub_category': device.sub_category,
                'serial_number': device.serial_number,
                'owner_name': device.owner_name,
                'supplier_name': device.supplier.name,
            }
            device_list.append(device_dict)

        # Convert the list of suppliers to JSON and add it to the context
        context['devices_json'] = json.dumps(device_list)

        return context


class CreateBusinessView(views.CreateView):
    queryset = Business.objects.all()
    template_name = 'business/create-business.html'
    form_class = CreateBusinessForm

    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class EditBusinessView(views.UpdateView):
    queryset = Business.objects.all()
    form_class = EditBusinessForm
    template_name = 'business/edit-business.html'

    def get_success_url(self):
        """
        Returns the URL to redirect to after processing a valid form.
        """
        return reverse('business', kwargs={'pk': self.object.pk})
