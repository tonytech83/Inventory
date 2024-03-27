from django.contrib.auth import get_user_model

from django.views import generic as views
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.business.models import Business
from inventory.common.utils import get_device_status_counts
from inventory.devices.models import Device
from inventory.suppliers.models import Supplier

UserModel = get_user_model()


class DashboardView(views.ListView):
    queryset = (Business.objects.all()
                .prefetch_related('device_set'))
    template_name = 'common/dashboard.html'


class ChartData(APIView):
    def get(self, request, format=None):
        business_names = [b.business_name for b in Business.objects.all()]
        devices_per_business = [b.device_set.count() for b in Business.objects.all()]
        colors = ["#FF6384", "#36A2EB", "#FFCE56", "#cc65fe", "#ff6347", "#36a2eb", "#ffd700"]
        status_labels, status_data = get_device_status_counts()

        data = {
            'labels': business_names,
            'devices': devices_per_business,
            'colors': colors[:len(business_names)],
            'status_labels': status_labels,
            'status_data': status_data,
        }

        return Response(data)


class HomeView(views.ListView):
    queryset = (Business.objects.all()
                .prefetch_related('device_set'))

    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owned_businesses'] = self.queryset.filter(owner=self.request.user)
        context['not_owned_businesses'] = (self.queryset
                                           .exclude(owner=self.request.user)
                                           .filter(is_visible=True))
        context['all_devices'] = Device.objects.all().count()
        context['all_engineers'] = UserModel.objects.count()
        context['total_suppliers'] = Supplier.objects.count()

        return context
