# Generated by Django 4.2 on 2023-05-25 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_alter_dtrsummary_nd_ot_total_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtrsummary',
            name='is_sched_restday',
            field=models.BooleanField(default=False),
        ),
    ]
