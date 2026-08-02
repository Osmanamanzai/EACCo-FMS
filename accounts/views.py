from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date
from collections import defaultdict
from transactions.models import Transaction
import json

SHAMSI_MONTHS = [
    '', 'حمل', 'ثور', 'جوزا', 'سرطان', 'اسد', 'سنبله',
    'میزان', 'عقرب', 'قوس', 'جدی', 'دلو', 'حوت'
]

def gregorian_to_shamsi_month(d):
    """Return (shamsi_year, shamsi_month) for a given Gregorian date."""
    nowruz = date(d.year, 3, 21)
    if d >= nowruz:
        sh_year = d.year - 621
        start = nowruz
    else:
        sh_year = d.year - 622
        start = date(d.year - 1, 3, 21)
    days = (d - start).days
    month_lengths = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
    month = 0
    while month < 11 and days >= month_lengths[month]:
        days -= month_lengths[month]
        month += 1
    return sh_year, month + 1

@login_required
def dashboard(request):
    # totals
    income_total = Transaction.objects.filter(type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    expense_total = Transaction.objects.filter(type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
    profit = income_total - expense_total

    # recent transactions
    recent = Transaction.objects.select_related('project', 'category').order_by('-date', '-created_at')[:10]

    # monthly chart data (last 6 Shamsi months)
    today = date.today()
    sh_year, sh_month = gregorian_to_shamsi_month(today)

    months_list = []
    for i in range(5, -1, -1):
        m = sh_month - i
        y = sh_year
        if m <= 0:
            m += 12
            y -= 1
        months_list.append((y, m))

    income_by_month = defaultdict(float)
    expense_by_month = defaultdict(float)

    for tx in Transaction.objects.filter(type='INCOME'):
        y, m = gregorian_to_shamsi_month(tx.date)
        income_by_month[(y, m)] += float(tx.amount)

    for tx in Transaction.objects.filter(type='EXPENSE'):
        y, m = gregorian_to_shamsi_month(tx.date)
        expense_by_month[(y, m)] += float(tx.amount)

    labels = []
    income_data = []
    expense_data = []
    for y, m in months_list:
        labels.append(SHAMSI_MONTHS[m])
        income_data.append(income_by_month.get((y, m), 0))
        expense_data.append(expense_by_month.get((y, m), 0))

    chart_json = json.dumps({
        'labels': labels,
        'income': income_data,
        'expense': expense_data,
    })

    context = {
        'total_income': income_total,
        'total_expense': expense_total,
        'profit': profit,                # ← now passed to template
        'recent_transactions': recent,
        'chart_data_json': chart_json,
    }
    return render(request, 'dashboard.html', context)