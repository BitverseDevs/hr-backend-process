# Generated by Django 4.2 on 2023-05-16 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_schedule_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Schedule',
            new_name='ScheduleShift',
        ),
        migrations.AlterModelTable(
            name='dtr',
            table='TBL_DTR_ENTRY',
        ),
        migrations.CreateModel(
            name='ScheduleDaily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_datetime', models.DateTimeField()),
                ('sched_dutyin', models.TimeField()),
                ('sched_dutyout', models.TimeField()),
                ('is_processed', models.BooleanField(blank=True, null=True)),
                ('is_current', models.BooleanField(blank=True, null=True)),
                ('employee_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employee', to_field='employee_number')),
            ],
            options={
                'db_table': 'TBL_SCHED_DAILY',
            },
        ),
    ]
