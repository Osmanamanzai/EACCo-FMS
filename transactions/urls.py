from django.urls import path
from . import views

urlpatterns = [
    # Expenses
    path('', views.expense_list, name='expense_list'),
    path('add/', views.expense_add, name='expense_add'),

    # Cash IN
    path('cash-in/', views.cash_in_list, name='cash_in_list'),
    path('cash-in/add/', views.cash_in_add, name='cash_in_add'),

    # Cash OUT
    path('cash-out/', views.cash_out_list, name='cash_out_list'),
    path('cash-out/add/', views.cash_out_add, name='cash_out_add'),

    # Edit / Delete (admin only) – works for both income and expense
    path('<int:pk>/edit/', views.transaction_update, name='transaction_update'),
    path('<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
]