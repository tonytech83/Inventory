from django.urls import reverse_lazy
from django.views import generic as views

from inventory.business.forms import CreateBusinessForm
from inventory.business.models import Business


class BusinessView(views.DetailView):
    queryset = Business.objects.all()
    template_name = 'business/business.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = context['business']
        context['devices'] = business.device_set.all()

        return context


class CreateBusinessView(views.CreateView):
    queryset = Business.objects.all()
    template_name = 'business/create-business.html'
    form_class = CreateBusinessForm

    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
