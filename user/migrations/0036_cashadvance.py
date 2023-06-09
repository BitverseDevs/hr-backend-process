# Generated by Django 4.2 on 2023-06-07 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0035_employee_accnt_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashAdvance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('cash_advance_total', models.FloatField()),
                ('cash_advance_remaining', models.FloatField()),
                ('payment_monthly', models.FloatField()),
                ('is_fully_paid', models.BooleanField(default=False)),
                ('last_payment_amount', models.FloatField(blank=True, null=True)),
                ('date_last_payment', models.DateField(blank=True, null=True)),
                ('emp_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employee', to_field='emp_no')),
            ],
            options={
                'db_table': 'TBL_CASH_ADVANCE',
            },
        ),
    ]
