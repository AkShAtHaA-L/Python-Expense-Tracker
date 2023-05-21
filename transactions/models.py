from django.db import models
from django.contrib.auth.models import User


TRANSACTION_CHOICES = [
    ("Expense","Expense"),
    ("Income", "Income")
]

CATEGORY_CHOICES = [
    ("Food and groceries", "Food and groceries"),
    ("Salary","Salary"),
    ("Bills", "Bills"),
    ("Shopping", "Shopping"),
    ("Investment","Investment"),
    ("Travel","Travel"),
    ("Others","Others")

]

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    type = models.CharField(max_length = 10 , choices=TRANSACTION_CHOICES)
    amount = models.FloatField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    comment = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.comment
