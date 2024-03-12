from django import forms

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
