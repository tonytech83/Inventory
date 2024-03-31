from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from inventory.organization.forms import OrganizationCreateForm, OrganizationEditForm
from inventory.organization.models import Organization


class CreateOrganizationView(auth_mixins.LoginRequiredMixin, views.CreateView):
    queryset = Organization.objects.all()
    template_name = 'organization/create-organization-page.html'
    form_class = OrganizationCreateForm

    def get_template_names(self):
        user = self.request.user
        organization = Organization.objects.exists()

        if user.is_superuser and organization:
            template_name = 'organization/organization-created.html'
        else:
            template_name = self.template_name

        return [template_name]


class EditOrganizationView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    queryset = Organization.objects.all()
    form_class = OrganizationEditForm
    template_name = 'organization/edit-organization-page.html'

    success_url = reverse_lazy('home-page')
