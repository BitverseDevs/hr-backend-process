# Generated by Django 4.2 on 2023-05-30 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_alter_employee_suffix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleshift',
            name='grace_period',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
