# Generated by Django 4.2 on 2023-05-24 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_leaves_leave_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaves',
            name='leave_approver2_empno',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
