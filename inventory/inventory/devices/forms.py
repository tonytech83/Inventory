from django import forms
from django.db import transaction

from inventory.devices.models import Device, Risk, Support


class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = '__all__'


class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = '__all__'


class DeviceBaseForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'


class DeviceCreateForm(DeviceBaseForm):
    class Meta:
        model = Device
        exclude = ('support', 'risk', 'business')

    # def __init__(self, *args, **kwargs):
    #     super(DeviceCreateForm, self).__init__(*args, **kwargs)
    #     # Initialize nested forms
    #     if self.instance.pk:
    #         # If editing an existing Device, populate the nested forms with related instances
    #         self.fields['risk_form'] = RiskForm(instance=self.instance.risk, prefix='risk')
    #         self.fields['support_form'] = SupportForm(instance=self.instance.support, prefix='support')
    #     else:
    #         # For a new Device, instantiate empty nested forms
    #         self.fields['risk_form'] = RiskForm(prefix='risk')
    #         self.fields['support_form'] = SupportForm(prefix='support')
    #
    # @transaction.atomic
    # def save(self, commit=True):
    #     instance = super(DeviceCreateForm, self).save(commit=False)
    #
    #     # Manually save nested forms
    #     risk = self.fields['risk_form'].save(commit=False)
    #     support = self.fields['support_form'].save(commit=False)
    #
    #     if commit:
    #         instance.save()
    #         risk.device = instance  # Assuming Risk has a FK to Device
    #         risk.save()
    #         support.device = instance  # Assuming Support has a FK to Device
    #         support.save()
    #
    #     return instance
