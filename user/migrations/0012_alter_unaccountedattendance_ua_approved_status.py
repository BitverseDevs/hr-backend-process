# Generated by Django 4.2 on 2023-05-24 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_unaccountedattendance_ua_approver1_empno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unaccountedattendance',
            name='ua_approved_status',
            field=models.CharField(choices=[('P1', 'Pending'), ('P2', 'Pending2'), ('APD', 'Approved'), ('DIS', 'Disapproved')], max_length=3),
        ),
    ]