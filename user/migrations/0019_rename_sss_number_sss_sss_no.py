# Generated by Django 4.2 on 2023-05-26 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_alter_employee_approver'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sss',
            old_name='sss_number',
            new_name='sss_no',
        ),
    ]