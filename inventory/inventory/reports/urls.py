from django.urls import path

from inventory.reports.views import ReportConfigurationView

urlpatterns = (
    path('', ReportConfigurationView.as_view(), name='edit-report'),
)
