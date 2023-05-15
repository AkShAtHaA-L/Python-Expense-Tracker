from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from users.models import User
from .models import Transaction
from django.utils import timezone
import datetime
from django.db.models import Sum

# Create your views here.

@login_required
def dashboard(request):
    user = User.objects.get(pk=request.user.id)

    #all transactions
    all_transactions = user.transaction_set.filter(type="Expense")
    all_transactions_sum = all_transactions.aggregate(Sum('amount'))['amount__sum']

    #last year expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    last_year_data = user.transaction_set.filter(date__gt=last_year,type="Expense")
    last_year_sum = last_year_data.aggregate(Sum('amount'))['amount__sum']
    
    #monthly expenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    last_month_data = user.transaction_set.filter(date__gt=last_month,type="Expense")
    last_month_sum = last_month_data.aggregate(Sum('amount'))['amount__sum']
    latest_five = all_transactions[0:5]
    
    monthly_budget = user.profile.monthly_budget
    context = {
        'username': user,
        'latest_five': latest_five,
        'monthly_budget': monthly_budget,
        'all_transactions_sum': all_transactions_sum,
        'last_month_sum': last_month_sum
    }
    return render(request, "transactions/index.html", context=context)


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
            print(transaction_object)
        else:
            print("Nope!")
    else:
        form = TransactionForm()
    return render(request, "transactions/newtransaction.html", {'form': form})