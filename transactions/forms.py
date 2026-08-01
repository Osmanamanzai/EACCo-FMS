from django import forms
from .models import Transaction, ExpenseCategory

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['project', 'category', 'amount', 'date', 'description', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ExpenseCategory.objects.all()


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['project', 'amount', 'date', 'description', 'receipt']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }