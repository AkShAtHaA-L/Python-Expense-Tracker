from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_budget = models.FloatField()

    def __str__(self):
        return self.user.username