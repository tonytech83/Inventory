from django import forms

from inventory.core.form_mixins import ReadOnlyFieldsFormMixin
from inventory.devices.models import Device


# class RiskForm(forms.ModelForm):
#     class Meta:
#         model = Risk
#         fields = '__all__'
#
#
# class SupportForm(forms.ModelForm):
#     class Meta:
#         model = Support
#         fields = '__all__'


# class DeviceBaseForm(forms.ModelForm):
#     class Meta:
#         model = Device
#         fields = '__all__'
#
#
# class DeviceCreateForm(DeviceBaseForm):
#     class Meta:
#         model = Device
#         exclude = ('support', 'risk', 'business')
#
#
# class DeviceEditForm(DeviceBaseForm):
#     class Meta:
#         model = Device
#         exclude = ('support', 'risk',)
#
#
# class DeviceDeleteForm(ReadOnlyFieldsFormMixin, DeviceBaseForm):
#     # TODO: Fix the Mixin if readonly_fields is '__all__' to made all fields readonly
#     readonly_fields = ('support', 'risk', 'business')
#
#     class Meta:
#         model = Device
#         exclude = ('support', 'risk', 'supplier', 'business')
#
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#
#
# class CSVUploadForm(forms.Form):
#     """
#     CSV upload form
#     """
#     csv_file = forms.FileField()
