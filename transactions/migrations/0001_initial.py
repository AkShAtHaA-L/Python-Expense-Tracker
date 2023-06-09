# Generated by Django 4.2 on 2023-05-07 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Expense', 'Expense'), ('Income', 'Income')], max_length=10)),
                ('amount', models.FloatField()),
                ('category', models.CharField(choices=[('Food and groceries', 'Food and groceries'), ('Bills', 'Bills'), ('Shopping', 'Shopping'), ('Investment', 'Investment'), ('Travel', 'Travel'), ('Others', 'Others')], max_length=20)),
                ('comment', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
