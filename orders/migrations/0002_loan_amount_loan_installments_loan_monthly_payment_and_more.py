# Generated by Django 5.0.1 on 2025-03-22 06:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='loan',
            name='installments',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='loan',
            name='monthly_payment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='loan',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'در انتظار پرداخت'), ('processing', 'در حال پردازش'), ('completed', 'تکمیل شده'), ('cancelled', 'لغو شده')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='loan',
            name='prepayment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
