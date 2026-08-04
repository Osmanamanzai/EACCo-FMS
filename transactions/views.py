from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from projects.models import Project
from .models import Transaction
from .forms import ExpenseForm, IncomeForm


@login_required
def expense_list(request):
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
        form = ExpenseForm(request.POST, request.FILES)
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
    })


# ---------- EDIT & DELETE (Admin only) ----------
@login_required
def transaction_update(request, pk):
    if not (request.user.is_admin() or request.user.is_superuser):
        raise PermissionDenied

    transaction = get_object_or_404(Transaction, pk=pk)
    if transaction.type == Transaction.Type.INCOME:
        form_class = IncomeForm
        cancel_url = reverse('cash_in_list')
    else:
        form_class = ExpenseForm
        cancel_url = reverse('cash_out_list')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully.')
            return redirect(cancel_url)
    else:
        form = form_class(instance=transaction)

    return render(request, 'transactions/cash_form.html', {
        'form': form,
        'title': 'Edit Transaction',
        'cancel_url': cancel_url,
    })


@login_required
def transaction_delete(request, pk):
    if not (request.user.is_admin() or request.user.is_superuser):
        raise PermissionDenied

    transaction = get_object_or_404(Transaction, pk=pk)
    if transaction.type == Transaction.Type.INCOME:
        cancel_url = reverse('cash_in_list')
    else:
        cancel_url = reverse('cash_out_list')

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted.')
        return redirect(cancel_url)

    return render(request, 'transactions/transaction_confirm_delete.html', {
        'transaction': transaction,
        'cancel_url': cancel_url,
    })