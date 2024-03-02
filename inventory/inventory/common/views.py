from django.views import generic as views

from inventory.business.models import Business


class DashboardView(views.TemplateView):
    template_name = 'common/dashboard.html'


class HomeView(views.ListView):
    queryset = Business.objects.all()
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owned_businesses'] = self.queryset.filter(owner=self.request.user)
        context['not_owned_businesses'] = self.queryset.exclude(owner=self.request.user)

        return context
