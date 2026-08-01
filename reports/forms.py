from django import forms
from projects.models import Project

class ReportFilterForm(forms.Form):
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        empty_label="All Projects"
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )