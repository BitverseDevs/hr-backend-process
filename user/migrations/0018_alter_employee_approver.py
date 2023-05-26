# Generated by Django 4.2 on 2023-05-26 08:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_dtrsummary_is_ua_dtrsummary_undertime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='approver',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9990)]),
        ),
    ]
