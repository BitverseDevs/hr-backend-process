# Generated by Django 4.2 on 2023-06-02 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_alter_dtrsummary_sched_timein_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dtrcutoff',
            name='emp_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employee', to_field='emp_no'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='civil_status',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(max_length=1),
        ),
    ]
