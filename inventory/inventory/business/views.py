from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from inventory.business.forms import CreateBusinessForm
from inventory.business.models import Business


class CreateBusinessView(views.CreateView):
    queryset = Business.objects.all()
    template_name = 'business/create-business.html'
    form_class = CreateBusinessForm

    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class BusinessView(views.DetailView):
    queryset = ...