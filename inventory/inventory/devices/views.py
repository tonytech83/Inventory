from django.http import FileResponse
import openpyxl

from django.conf import settings
import os

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic.edit import FormView
from django.contrib import messages

from inventory.business.models import Business
from inventory.devices.forms import DeviceCreateForm, RiskForm, SupportForm, DeviceEditForm, DeviceDeleteForm, \
    CSVUploadForm
from inventory.devices.models import Device, Support, Risk
from inventory.suppliers.models import Supplier


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


# TODO: Check for login permissions
class DeviceEditView(views.UpdateView):
    queryset = (Device.objects.all()
                .prefetch_related('support')
                .prefetch_related('risk'))

    form_class = DeviceEditForm
    template_name = 'devices/edit-device.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'support_form' not in context:
            context['support_form'] = SupportForm(instance=self.object.support)
        if 'risk_form' not in context:
            context['risk_form'] = RiskForm(instance=self.object.risk)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        support_form = SupportForm(request.POST, instance=self.object.support)
        risk_form = RiskForm(request.POST, instance=self.object.risk)

        if form.is_valid() and support_form.is_valid() and risk_form.is_valid():
            return self.form_valid(form, support_form, risk_form)
        else:
            return self.form_invalid(form, support_form, risk_form)

    def form_valid(self, form, support_form, risk_form):
        self.object = form.save()
        support_form.save()
        risk_form.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form, support_form, risk_form):
        return self.render_to_response(
            self.get_context_data(form=form, support_form=support_form, risk_form=risk_form))

    def get_success_url(self):
        # Redirect to the business detail page
        return reverse_lazy('business', kwargs={'pk': self.object.business_id})


class DeviceDeleteView(views.DeleteView):
    queryset = Device.objects.all()
    form_class = DeviceDeleteForm
    template_name = 'devices/delete-device.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object

        return kwargs

    def get_success_url(self):
        # Redirect to the business detail page
        return reverse_lazy('business', kwargs={'pk': self.object.business_id})


class CSVUploadView(FormView):
    template_name = 'business/upload-devices.html'
    form_class = CSVUploadForm

    def get_success_url(self):
        # Redirect to the business page
        return reverse_lazy('business', kwargs={'pk': self.kwargs.get('business_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs.get('business_id')

        return context

    def form_valid(self, form):
        # Handle the uploaded file
        uploaded_file = form.cleaned_data['csv_file']
        wb = openpyxl.load_workbook(uploaded_file)
        sheet = wb.active
        business_id = self.kwargs.get('business_id')
        business = get_object_or_404(Business, pk=business_id)

        for row in sheet.iter_rows(min_row=3):  # Skip the first two header rows
            try:
                # Create a new Support object for every device
                support = Support.objects.create(
                    support_model=row[14].value if row[14].value else "Default Support Model",
                    purchase_order_number=row[15].value,
                    invoice_img=row[16].value or 'Not set',
                    # TODO: Fix this dates
                    sos=row[17].value or '2024-03-10',
                    eos=row[18].value or '2024-03-10',
                    eol=row[19].value or '2024-03-10',
                )

                # Create a new Risk object for every device
                risk = Risk.objects.create(
                    business_processes_at_risk=row[20].value if row[20].value else "Default Risk",
                    impact=row[21].value or 1,
                    likelihood=row[22].value or 1,
                )

                Device.objects.create(
                    device_name=row[0].value,
                    domain=row[1].value,
                    description=row[2].value,
                    status=row[3].value,
                    category=row[4].value,
                    sub_category=row[5].value,
                    manufacturer=row[6].value,
                    model=row[7].value,
                    ip_address=row[8].value,
                    ip_address_sec=row[9].value,
                    serial_number=row[10].value,
                    operating_system=row[11].value,
                    building=row[12].value,
                    owner_name=row[13].value,
                    support=support,
                    risk=risk,
                    business=business,
                    # supplier=Supplier.objects.all().first(),
                )
            except Exception as e:
                print(e)
                continue

        messages.success(self.request, "Devices imported successfully.")
        return super().form_valid(form)


def download_template(request):
    # Define the path to the template
    template_path = os.path.join(settings.BASE_DIR, 'staticfiles', 'template_file', 'template.xlsx')

    # Open the file for reading
    excel = open(template_path, 'rb')
    response = FileResponse(excel)

    # Set the content-type and disposition to prompt download
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response['Content-Disposition'] = 'attachment; filename=template.xlsx'
    return response
