from django.db import models
from django.conf import settings
from projects.models import Project

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Expense Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Transaction(models.Model):
    class Type(models.TextChoices):
        INCOME = 'INCOME', 'Income'
        EXPENSE = 'EXPENSE', 'Expense'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.EXPENSE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 help_text="Required for expenses")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    receipt = models.FileField(upload_to='receipts/%Y/%m/', blank=True, null=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} AFN - {self.project.name}"