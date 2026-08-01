from django.urls import path
from . import views

urlpatterns = [
    # Expenses (already exists)
    path('', views.expense_list, name='expense_list'),
    path('add/', views.expense_add, name='expense_add'),

    # Cash IN
    path('cash-in/', views.cash_in_list, name='cash_in_list'),
    path('cash-in/add/', views.cash_in_add, name='cash_in_add'),

    # Cash OUT
    path('cash-out/', views.cash_out_list, name='cash_out_list'),
    path('cash-out/add/', views.cash_out_add, name='cash_out_add'),
]