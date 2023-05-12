from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm
from users.models import User
from .models import Transaction

# Create your views here.

@login_required
def dashboard(request):
    user = User.objects.get(pk=request.user.id)
    all_transactions = user.transaction_set.all()
    for transaction in all_transactions:
        print(transaction)
    context = {
        'all_transactions': all_transactions
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