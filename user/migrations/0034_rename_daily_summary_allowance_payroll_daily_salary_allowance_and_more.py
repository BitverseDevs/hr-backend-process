# Generated by Django 4.2 on 2023-06-07 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0033_rename_pagibig_amount_d_payroll_pagibigc_amount_d_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payroll',
            old_name='daily_summary_allowance',
            new_name='daily_salary_allowance',
        ),
        migrations.RenameField(
            model_name='payroll',
            old_name='daily_summary_basic',
            new_name='daily_salary_basic',
        ),
        migrations.RenameField(
            model_name='payroll',
            old_name='daily_summary_other',
            new_name='daily_salary_other',
        ),
    ]