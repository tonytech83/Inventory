from django.urls import reverse_lazy, reverse
from django.views import generic as views

from inventory.business.forms import CreateBusinessForm, EditBusinessForm
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


class EditBusinessView(views.UpdateView):
    queryset = Business.objects.all()
    form_class = EditBusinessForm
    template_name = 'business/edit-business.html'

    def get_success_url(self):
        """
        Returns the URL to redirect to after processing a valid form.
        """
        return reverse('business', kwargs={'pk': self.object.pk})
