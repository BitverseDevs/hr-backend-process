# Generated by Django 4.2 on 2023-05-25 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_dtrsummary_paid_leave_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtrsummary',
            name='nd_ot_total',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dtrsummary',
            name='reg_ot_total',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
