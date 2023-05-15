# Generated by Django 4.2 on 2023-05-15 06:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_rename_paid_leave_dtrsummary_is_paid_leave_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('time_in', models.TimeField()),
                ('time_out', models.TimeField()),
                ('grace_period', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('with_overtime', models.BooleanField()),
                ('is_night_shift', models.BooleanField()),
            ],
            options={
                'db_table': 'TBL_SCHEDULE_SHIFT',
            },
        ),
        migrations.RenameField(
            model_name='dtrsummary',
            old_name='ot_approved',
            new_name='is_ot_approved',
        ),
        migrations.AlterField(
            model_name='pagibig',
            name='pagibig_contribution_month',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pagibig',
            name='pagibig_rem_cloan_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pagibig',
            name='pagibig_rem_hloan_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pagibig',
            name='pagibig_with_cloan_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pagibig',
            name='pagibig_with_hloan_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sss',
            name='sss_contribution_month',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sss',
            name='sss_rem_callloan_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sss',
            name='sss_rem_cashloan_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sss',
            name='sss_with_calloan_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sss',
            name='sss_with_cashloan_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tax',
            name='payment_frequency',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Semi-Monthly'), (2, 'Monthly'), (3, 'Annual')], null=True, validators=[django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.AlterField(
            model_name='tax',
            name='tax_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tax',
            name='tax_form',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='tax',
            name='tax_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Philhealth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ph_number', models.CharField(max_length=10)),
                ('ph_contribution_month', models.FloatField(blank=True, null=True)),
                ('ph_category', models.CharField(blank=True, max_length=10, null=True)),
                ('employee_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employee', to_field='employee_number')),
            ],
            options={
                'db_table': 'TBL_PHILHEALTH_CODE',
            },
        ),
        migrations.CreateModel(
            name='Cutoff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('co_name', models.CharField(max_length=20)),
                ('co_description', models.TextField(max_length=75)),
                ('co_date', models.DateTimeField()),
                ('co_date_from', models.DateTimeField()),
                ('co_date_to', models.DateTimeField()),
                ('co_is_processed', models.BooleanField()),
                ('credit_date', models.DateTimeField()),
                ('payroll_frequency', models.PositiveSmallIntegerField(choices=[(1, 'Monthly'), (2, 'Semi-Monthly'), (3, 'Project-Based'), (4, 'Weekly')], validators=[django.core.validators.MaxValueValidator(4)])),
                ('division_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.division')),
                ('payroll_group_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.payrollgroup')),
            ],
            options={
                'db_table': 'TBL_CUTOFF_PERIOD_LIST',
            },
        ),
    ]
