# Generated by Django 4.2 on 2023-05-25 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_rename_ua_approved_status_unaccountedattendance_ua_approval_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtrsummary',
            name='paid_leave_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]