from django import forms

from inventory.reports.models import Report


class ReportConfigurationFrom(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['turn_on', 'day_of_week']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
        }
