from django.contrib import admin
from .models import Transaction, ExpenseCategory

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('project', 'type', 'category', 'amount', 'date', 'added_by')
    list_filter = ('type', 'project', 'category')
    search_fields = ('description', 'project__name')
    date_hierarchy = 'date'

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ExpenseCategory)