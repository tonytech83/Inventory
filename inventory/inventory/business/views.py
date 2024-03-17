import json
from datetime import timedelta

from rest_framework import generics as api_views

from django.db.models import Case, When, Value, IntegerField, ExpressionWrapper, F
from django.db.models.functions import Now
from django.forms import DurationField, BooleanField
from django.utils.timezone import now

from django.urls import reverse_lazy, reverse
from django.views import generic as views
from rest_framework.permissions import IsAuthenticated

from inventory.business.forms import CreateBusinessForm, EditBusinessForm
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
                'is_reviewed': device.is_reviewed,
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
                'eos': str(device.support.eos),
            }
            device_list.append(device_dict)

        # Convert the list of suppliers to JSON and add it to the context
        context['devices_json'] = json.dumps(device_list)

        return context


# class CreateBusinessView(views.CreateView):
#     queryset = Business.objects.all()
#     template_name = 'business/create-business.html'
#     form_class = CreateBusinessForm
#
#     success_url = reverse_lazy('home-page')
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)

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
