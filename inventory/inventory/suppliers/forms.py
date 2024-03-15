from django import forms

from inventory.core.form_mixins import ReadOnlyFieldsFormMixin
from inventory.suppliers.models import Supplier


class SupplierBaseForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class CreateSupplierForm(SupplierBaseForm):
    pass


class EditSupplierForm(SupplierBaseForm):
    class Meta:
        model = Supplier
        exclude = ('name',)


class DeviceSupplierForm(ReadOnlyFieldsFormMixin, SupplierBaseForm):
    # TODO: Fix the Mixin if readonly_fields is '__all__' to made all fields readonly
    readonly_fields = ('name', 'contact_name', 'phone_number', 'email')

    class Meta:
        model = Supplier
        exclude = ('support', 'risk', 'supplier', 'business')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
