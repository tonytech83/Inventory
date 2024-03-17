import json
from datetime import timedelta

from rest_framework import generics as api_views

from django.utils.timezone import now

from django.urls import reverse
from django.views import generic as views
from rest_framework.permissions import IsAuthenticated

from inventory.business.forms import EditBusinessForm
from inventory.business.models import Business
from inventory.business.serializers import BusinessSerializer


class BusinessView(views.DetailView):
    template_name = 'business/business.html'

    def get_queryset(self):
        return Business.objects.all().prefetch_related(
            'device_set',
            'device_set__support',
            'device_set__risk',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = context['object']
        no_support = self.request.GET.get('no_support', None)
        no_reviewed = self.request.GET.get('no_reviewed', None)

        device_queryset = business.device_set.all()

        if no_support == 'true':
            device_queryset = device_queryset.filter(support__eos__lt=now().date())

        if no_reviewed == 'true':
            one_year_ago = now() - timedelta(days=365)
            device_queryset = device_queryset.filter(updated_at__lte=one_year_ago)

        device_list = []

        for device in device_queryset:
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
                'supplier_name': device.supplier_display,
            }
            device_list.append(device_dict)

        # Convert the list of suppliers to JSON and add it to the context
        context['devices_json'] = json.dumps(device_list)

        return context


class CreateBusinessApiView(api_views.CreateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EditBusinessView(views.UpdateView):
    queryset = Business.objects.all()
    form_class = EditBusinessForm
    template_name = 'business/edit-business.html'

    def get_success_url(self):
        """
        Returns the URL to redirect to after processing a valid form.
        """
        return reverse('business', kwargs={'pk': self.object.pk})
