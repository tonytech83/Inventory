from django import forms

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
