from django.contrib.auth import get_user_model
from django.views import generic as views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.business.models import Business
from inventory.common.utils import (
    get_business_by_categories,
    get_device_status_counts,
    get_devices_support_count,
)
from inventory.devices.models import Device
from inventory.suppliers.models import Supplier

UserModel = get_user_model()


class DashboardView(views.ListView):
    queryset = Business.objects.all().prefetch_related("device_set")
    template_name = "common/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["is_data"] = Device.objects.all()

        return context


class ChartData(APIView):
    """
    API view that aggregates data for Chart.js based on the business, device status, support status,
    and device categories.

    Returns:
        Response: A Django REST framework Response object containing the chart data as a JSON object.

    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        business_names = [b.business_name for b in Business.objects.all()]
        devices_per_business = [b.device_set.count() for b in Business.objects.all()]
        status_labels, status_data = get_device_status_counts()
        support_labels, support_data = get_devices_support_count()
        categories_data, category_labels = get_business_by_categories()

        colors = [
            f"rgba({(idx + 10) * 30 % 255}, {(idx + 10) * 60 % 255}, {(idx + 10) * 90 % 255}, 0.5)"
            for idx in range(len(category_labels))
        ]

        data = {
            "labels": business_names,
            "devices": devices_per_business,
            "colors": colors,
            "status_labels": status_labels,
            "status_data": status_data,
            "support_labels": support_labels,
            "support_data": support_data,
            "categories_data": categories_data,
            "category_labels": category_labels,
        }

        return Response(data)


class HomeView(views.ListView):
    queryset = Business.objects.all().prefetch_related("device_set")

    template_name = "common/home-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owned_businesses"] = self.queryset.filter(owner=self.request.user)
        context["not_owned_businesses"] = self.queryset.exclude(
            owner=self.request.user
        ).filter(is_visible=True)
        context["all_devices"] = Device.objects.all().count()
        context["all_engineers"] = UserModel.objects.count()
        context["total_suppliers"] = Supplier.objects.count()

        return context
