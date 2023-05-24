from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from users.models import User
from .models import Transaction
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.core.paginator import Paginator

# Create your views here.

#Set a monthly budget, show last 7 days data in the dashboard
@login_required
def dashboard(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == "POST" and "monthly_budget" in request.POST:
        updated_budget = request.POST.get("monthly_budget")
        user.profile.monthly_budget = updated_budget
        user.save()
    
    #One week expenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    last_week_data = user.transaction_set.filter(date__gt=last_week,type="Expense")
    
    #split to pages
    paginator = Paginator(last_week_data, 5)
    page = request.GET.get('page')
    last_week_data = paginator.get_page(page)
    monthly_budget = user.profile.monthly_budget
    context = {
        'username': user,
        'last_week_data': last_week_data,
        'monthly_budget': monthly_budget,
    }
    return render(request, "transactions/index.html", context=context)


#Add a new transaction to the database
@login_required
def newentry(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            user_object = User.objects.get(pk=int(request.user.id))
            entered_type = form.cleaned_data.get("type")
            entered_amount = form.cleaned_data.get("amount")
            entered_category = form.cleaned_data.get("category")
            entered_comment = form.cleaned_data.get("comment")
            entered_date = form.cleaned_data.get("date")

            transaction_object = Transaction.objects.create(
                user =user_object,
                type = entered_type,
                amount = entered_amount,
                category = entered_category,
                comment = entered_comment,
                date = entered_date
            )
            messages.add_message(request, messages.INFO, "This transaction is added!")
        else:
            messages.add_message(request, messages.ERROR, f"{user_object} , Not a valid transaction!")
    else:
        form = TransactionForm()
    return render(request, "transactions/newtransaction.html", {'form': form})


@login_required
def allentries(request):
    user = User.objects.get(pk=request.user.id)
    monthly_budget = user.profile.monthly_budget

    #monthly expenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    last_month_expenses = user.transaction_set.filter(date__gt=last_month,type="Expense")
    last_month_income = user.transaction_set.filter(date__gt=last_month,type="Income")
    month_chart = {}
    for expense in last_month_expenses:
        if expense.category in month_chart:
            month_chart[expense.category] += expense.amount
        else:
            month_chart[expense.category] = expense.amount   
    last_month_expenses_sum = last_month_expenses.aggregate(Sum('amount'))['amount__sum']
    last_month_income_sum = last_month_income.aggregate(Sum('amount'))['amount__sum']

    #check budget
    if last_month_expenses_sum and last_month_expenses_sum >= monthly_budget:
        budget_exceeded = True
    else:
        budget_exceeded = False 

    #last year expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    last_year_expenses = user.transaction_set.filter(date__gt=last_year,type="Expense")
    last_year_income = user.transaction_set.filter(date__gt=last_year,type="Income")
    year_chart = {}
    for expense in last_year_expenses:
        if expense.category in year_chart:
            year_chart[expense.category] += expense.amount
        else:
            year_chart[expense.category] = expense.amount
    last_year_expenses_sum = last_year_expenses.aggregate(Sum('amount'))['amount__sum']
    last_year_income_sum = last_year_income.aggregate(Sum('amount'))['amount__sum']

    context = {
        'username': user,
        'month_labels': list(month_chart.keys()),
        'month_data': list(month_chart.values()),
        'year_labels': list(year_chart.keys()),
        'year_data': list(year_chart.values()),
        'month_expense_sum': last_month_expenses_sum,
        'month_income_sum': last_month_income_sum,
        'year_expense_sum': last_year_expenses_sum,
        'year_income_sum': last_year_income_sum,
        'budget_exceeded': budget_exceeded
    }
    return render(request, "transactions/allexpenses.html",context=context)


@login_required
def edit_entry(request, **kwargs):
    transaction_id = kwargs["id"]
    transaction_object = Transaction.objects.get(pk=transaction_id)
    form = TransactionForm(instance=transaction_object)
    if request.method == 'POST':
        updated_transaction = Transaction.objects.get(pk=transaction_id)
        form = TransactionForm(request.POST,instance=updated_transaction)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, "This transaction is updated!")
    
    context = {
        'form': form
    }
    return render(request, "transactions/edit.html",context=context)
    

@login_required
def delete_entry(request, **kwargs):
    if request.method =='POST' and 'delete_id' in request.POST:
        transaction_id = kwargs["id"]
        old_transaction = Transaction.objects.get(pk=transaction_id)
        old_transaction.delete()
    return redirect('dashboard')