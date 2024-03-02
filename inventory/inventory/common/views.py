from django.views import generic as views


class DashboardView(views.TemplateView):
    template_name = 'common/dashboard.html'


class HomeView(views.TemplateView):
    template_name = 'common/home-page.html'
