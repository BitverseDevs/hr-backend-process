# Generated by Django 4.2 on 2023-05-24 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_unaccountedattendance_ua_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unaccountedattendance',
            name='ua_approver1_empno',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
