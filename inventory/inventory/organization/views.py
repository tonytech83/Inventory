from django.urls import reverse_lazy
from django.views import generic as views

from inventory.organization.forms import OrganizationCreateForm, OrganizationEditForm
from inventory.organization.models import Organization


class CreateOrganizationView(views.CreateView):
    queryset = Organization.objects.all()
    template_name = 'organization/create-organization-page.html'
    form_class = OrganizationCreateForm

    success_url = reverse_lazy('home-page')


class EditOrganizationView(views.UpdateView):
    queryset = Organization.objects.all()
    form_class = OrganizationEditForm
    template_name = 'organization/edit-organization-page.html'

    success_url = reverse_lazy('home-page')
