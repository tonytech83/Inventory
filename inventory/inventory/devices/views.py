from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from inventory.business.models import Business
from inventory.devices.forms import DeviceCreateForm, RiskForm, SupportForm
from inventory.devices.models import Device


class DeviceCreateView(views.CreateView):
    model = Device
    form_class = DeviceCreateForm
    template_name = 'devices/create-device.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs.get('business_id')

        if 'risk_form' not in context:
            context['risk_form'] = RiskForm(self.request.POST or None, prefix='risk')
        if 'support_form' not in context:
            context['support_form'] = SupportForm(self.request.POST or None, prefix='support')

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        risk_form = context['risk_form']
        support_form = context['support_form']

        with transaction.atomic():
            """
            Use Django's transaction.atomic decorator to ensure that the entire operation is atomic.
            This means either all operations succeed, or none do, preventing database integrity errors.
            Additionally, save the Device instance only after the Risk and Support instances have been saved
            and associated with it.
            """
            if form.is_valid() and risk_form.is_valid() and support_form.is_valid():
                # Temporarily save the Device form without committing to the DB
                self.object = form.save(commit=False)
                # Save the Risk and Support forms and associate them with the Device
                risk = risk_form.save()
                support = support_form.save()
                self.object.risk = risk
                self.object.support = support

                # Capture the business_id from URL parameters and associate it with the device
                business_id = self.kwargs.get('business_id')
                business = get_object_or_404(Business, pk=business_id)
                self.object.business = business

                # Now save the Device object to the database
                self.object.save()

                return redirect(self.get_success_url())
            else:
                # If forms are not valid, return to the form with errors
                return self.form_invalid(form)

    def get_success_url(self):
        # Redirect to the business detail page
        return reverse_lazy('business', kwargs={'pk': self.kwargs.get('business_id')})
