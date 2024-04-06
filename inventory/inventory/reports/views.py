from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views

from inventory.reports.forms import ReportConfigurationFrom
from inventory.reports.models import Report


class ReportConfigurationView(LoginRequiredMixin, views.UpdateView):
    queryset = Report.objects.all()
    form_class = ReportConfigurationFrom
    template_name = 'reports/edit-report-page.html'

    success_url = reverse_lazy('home-page')

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            raise Http404

        return get_object_or_404(Report, profile__account=self.request.user)
