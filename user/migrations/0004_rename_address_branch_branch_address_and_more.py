# Generated by Django 4.2 on 2023-05-12 01:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_employee_pagibig_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='branch',
            old_name='address',
            new_name='branch_address',
        ),
        migrations.RenameField(
            model_name='branch',
            old_name='contact_number',
            new_name='branch_contact_number',
        ),
        migrations.RenameField(
            model_name='branch',
            old_name='email',
            new_name='branch_email',
        ),
        migrations.RenameField(
            model_name='branch',
            old_name='name',
            new_name='branch_name',
        ),
        migrations.RenameField(
            model_name='branch',
            old_name='oic',
            new_name='branch_oic',
        ),
        migrations.RenameField(
            model_name='citymunicipality',
            old_name='province',
            new_name='province_code',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='branch_code',
            new_name='dept_branch_code',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='lead',
            new_name='dept_lead',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='name',
            new_name='dept_name',
        ),
        migrations.RenameField(
            model_name='division',
            old_name='branch_code',
            new_name='div_branch_code',
        ),
        migrations.RenameField(
            model_name='division',
            old_name='lead',
            new_name='div_lead',
        ),
        migrations.RenameField(
            model_name='division',
            old_name='name',
            new_name='div_name',
        ),
        migrations.RenameField(
            model_name='dtr',
            old_name='processed',
            new_name='is_processed',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='email',
            new_name='email_address',
        ),
        migrations.AddField(
            model_name='employee',
            name='bio_id',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9990)]),
        ),
        migrations.AlterField(
            model_name='dtr',
            name='branch_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dtr', to='user.branch'),
        ),
        migrations.AlterField(
            model_name='dtr',
            name='business_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dtr',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='dtr',
            name='employee_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dtr', to='user.employee', to_field='employee_number'),
        ),
        migrations.AlterField(
            model_name='dtr',
            name='entry_type',
            field=models.CharField(blank=True, choices=[('DIN', 'Duty In'), ('DOUT', 'Duty Out'), ('LOUT', 'Lunch Out'), ('LIN', 'Lunch In')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='dtr',
            name='sched_timein',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dtr',
            name='sched_timeout',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterModelTable(
            name='holiday',
            table='TBL_HOLIDAY_TYPE',
        ),
    ]
