from django import forms
from .models import Project, ProjectDocument

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'location', 'start_date', 'end_date', 'budget', 'description', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ProjectDocumentForm(forms.ModelForm):
    class Meta:
        model = ProjectDocument
        fields = ['file']