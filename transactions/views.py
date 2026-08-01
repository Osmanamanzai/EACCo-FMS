from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import Project
from .models import Transaction
from .forms import ExpenseForm, IncomeForm

@login_required
def expense_list(request):
    # Get filter parameters
    project_id = request.GET.get('project', '')
    projects = Project.objects.all()
    expenses = Transaction.objects.filter(type=Transaction.Type.EXPENSE)

    if project_id:
        expenses = expenses.filter(project_id=project_id)
        selected_project = Project.objects.filter(pk=project_id).first()
    else:
        selected_project = None

    return render(request, 'transactions/expense_list.html', {
        'expenses': expenses,
        'projects': projects,
        'selected_project': selected_project,
    })

@login_required
def expense_add(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.type = Transaction.Type.EXPENSE
            expense.added_by = request.user
            expense.save()
            messages.success(request, 'Expense recorded successfully.')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'transactions/expense_form.html', {'form': form, 'title': 'Add New Expense'})


# ---------- Cash IN views ----------
@login_required
def cash_in_list(request):
    project_id = request.GET.get('project', '')
    projects = Project.objects.all()
    incomes = Transaction.objects.filter(type=Transaction.Type.INCOME)

    selected_project = None
    if project_id:
        incomes = incomes.filter(project_id=project_id)
        selected_project = Project.objects.filter(pk=project_id).first()

    return render(request, 'transactions/cash_in_list.html', {
        'incomes': incomes,
        'projects': projects,
        'selected_project': selected_project,
    })

@login_required
def cash_in_add(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST, request.FILES)
        if form.is_valid():
            income = form.save(commit=False)
            income.type = Transaction.Type.INCOME
            income.added_by = request.user
            income.save()
            messages.success(request, 'Cash IN recorded successfully.')
            return redirect('cash_in_list')
    else:
        form = IncomeForm()
    return render(request, 'transactions/cash_form.html', {
        'form': form,
        'title': 'Add Cash IN',
        'action_url': 'cash_in_add',
    })

# ---------- Cash OUT views ----------
@login_required
def cash_out_list(request):
    project_id = request.GET.get('project', '')
    projects = Project.objects.all()
    expenses = Transaction.objects.filter(type=Transaction.Type.EXPENSE)

    selected_project = None
    if project_id:
        expenses = expenses.filter(project_id=project_id)
        selected_project = Project.objects.filter(pk=project_id).first()

    return render(request, 'transactions/cash_out_list.html', {
        'expenses': expenses,
        'projects': projects,
        'selected_project': selected_project,
    })

@login_required
def cash_out_add(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)  # reuse expense form with categories
        if form.is_valid():
            expense = form.save(commit=False)
            expense.type = Transaction.Type.EXPENSE
            expense.added_by = request.user
            expense.save()
            messages.success(request, 'Cash OUT recorded successfully.')
            return redirect('cash_out_list')
    else:
        form = ExpenseForm()
    return render(request, 'transactions/cash_form.html', {
        'form': form,
        'title': 'Add Cash OUT',
        'action_url': 'cash_out_add',
    })