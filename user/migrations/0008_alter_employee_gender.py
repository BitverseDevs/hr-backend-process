# Generated by Django 4.2 on 2023-04-27 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.SmallIntegerField(choices=[(0, 'Female'), (1, 'Male')]),
        ),
    ]
