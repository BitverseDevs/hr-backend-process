# Generated by Django 4.2 on 2023-04-27 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_employee_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(choices=[('f', 'Female'), ('m', 'Male')], max_length=1),
        ),
    ]