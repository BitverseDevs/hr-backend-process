# Generated by Django 4.2 on 2023-05-30 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_alter_dtrsummary_sched_timein_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtrsummary',
            name='sched_timein',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dtrsummary',
            name='sched_timeout',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dtrsummary',
            name='shift_name',
            field=models.CharField(default='RD', max_length=25),
        ),
    ]
