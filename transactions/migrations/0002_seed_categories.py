from django.db import migrations

def create_categories(apps, schema_editor):
    ExpenseCategory = apps.get_model('transactions', 'ExpenseCategory')
    categories = [
        'Materials',
        'Transportation',
        'Kitchen',
        'Commissions',
        'TAX',
        'Administrative',
        'Rentals',
        'Documentations',
        'Utilities',
        'Payrolls',
        'Onsite Expenses',
    ]
    for cat in categories:
        ExpenseCategory.objects.get_or_create(name=cat)

def remove_categories(apps, schema_editor):
    ExpenseCategory = apps.get_model('transactions', 'ExpenseCategory')
    ExpenseCategory.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('transactions', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_categories, remove_categories),
    ]