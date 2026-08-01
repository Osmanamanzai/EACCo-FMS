from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from transactions.models import Transaction
from .forms import ReportFilterForm

@login_required
def report_view(request):
    form = ReportFilterForm(request.GET or None)
    incomes = Transaction.objects.filter(type=Transaction.Type.INCOME)
    expenses = Transaction.objects.filter(type=Transaction.Type.EXPENSE)

    if form.is_valid():
        project = form.cleaned_data.get('project')
        start = form.cleaned_data.get('start_date')
        end = form.cleaned_data.get('end_date')
        if project:
            incomes = incomes.filter(project=project)
            expenses = expenses.filter(project=project)
        if start:
            incomes = incomes.filter(date__gte=start)
            expenses = expenses.filter(date__gte=start)
        if end:
            incomes = incomes.filter(date__lte=end)
            expenses = expenses.filter(date__lte=end)

    context = {
        'form': form,
        'incomes': incomes,
        'expenses': expenses,
    }
    return render(request, 'reports/report.html', context)

@login_required
def report_pdf(request):
    form = ReportFilterForm(request.GET or None)
    incomes = Transaction.objects.filter(type=Transaction.Type.INCOME)
    expenses = Transaction.objects.filter(type=Transaction.Type.EXPENSE)

    # Validate the form first
    if form.is_valid():
        project = form.cleaned_data.get('project')
        start = form.cleaned_data.get('start_date')
        end = form.cleaned_data.get('end_date')
        if project:
            incomes = incomes.filter(project=project)
            expenses = expenses.filter(project=project)
        if start:
            incomes = incomes.filter(date__gte=start)
            expenses = expenses.filter(date__gte=start)
        if end:
            incomes = incomes.filter(date__lte=end)
            expenses = expenses.filter(date__lte=end)

        filters = {
            'project': project,
            'start_date': start,
            'end_date': end,
        }
    else:
        # If form is not valid (e.g., no parameters), use empty filters
        filters = {}

    template = get_template('reports/report_pdf.html')
    html = template.render({
        'incomes': incomes,
        'expenses': expenses,
        'filters': filters,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="EACCo_report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation error')
    return response






from accounts.models import User
u = User.objects.get(username='EACCo')
u.role = 'ADMIN'
u.save()
print(f'{u.username} is now {u.get_role_display()}')