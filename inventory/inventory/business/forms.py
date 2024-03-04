from django import forms

from inventory.business.models import Business


class BusinessBaseForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = '__all__'


class CreateBusinessForm(BusinessBaseForm):
    class Meta:
        model = Business
        exclude = ('owner',)


class EditBusinessForm(BusinessBaseForm):
    pass


class DeleteBusinessForm(BusinessBaseForm):
    pass



