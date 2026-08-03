from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from .models import Project
from .forms import ProjectForm, ProjectDocumentForm

def is_admin(user):
    return user.is_admin()


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def project_create(request):
    # Allow both admins (role) and superusers
    if not (request.user.is_admin() or request.user.is_superuser):
        raise PermissionDenied

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created successfully.')
            return redirect('project_detail', pk=project.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Add New Project'})


@login_required
def project_update(request, pk):
    # Allow both admins (role) and superusers
    if not (request.user.is_admin() or request.user.is_superuser):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Edit Project'})


@login_required
def project_delete(request, pk):
    # Allow both admins (role) and superusers
    if not (request.user.is_admin() or request.user.is_superuser):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    documents = project.documents.all()

    # Calculate financial totals
    total_income = project.transactions.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = project.transactions.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
    profit = total_income - total_expense

    # Document upload – only admins/superusers can upload
    if request.method == 'POST' and (request.user.is_admin() or request.user.is_superuser):
        doc_form = ProjectDocumentForm(request.POST, request.FILES)
        if doc_form.is_valid():
            doc = doc_form.save(commit=False)
            doc.project = project
            doc.save()
            messages.success(request, 'Document uploaded.')
            return redirect('project_detail', pk=pk)
        else:
            messages.error(request, 'Invalid file. Please try again.')
    else:
        doc_form = ProjectDocumentForm()

    context = {
        'project': project,
        'documents': documents,
        'doc_form': doc_form,
        'is_admin': request.user.is_admin() or request.user.is_superuser,  # show upload button if admin/superuser
        'total_income': total_income,
        'total_expense': total_expense,
        'profit': profit,
    }
    return render(request, 'projects/project_detail.html', context)