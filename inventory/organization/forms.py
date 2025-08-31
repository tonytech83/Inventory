from django import forms

from inventory.organization.models import Organization


class OrganizationBaseForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationCreateForm(OrganizationBaseForm):
    class Meta:
        model = Organization
        fields = (
            "organization_name",
            "region",
            "logo",
        )
        widgets = {
            "region": forms.Select(attrs={"class": "form-control"}),
        }


class OrganizationEditForm(OrganizationBaseForm):
    class Meta:
        model = Organization
        fields = (
            "organization_name",
            "region",
            "logo",
        )
        widgets = {
            "region": forms.Select(attrs={"class": "form-control"}),
        }
