# Generated by Django 4.2 on 2023-05-04 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0032_rename_date_obt_date_filed_obt_cutoff_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='obt',
            name='employee_number',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user.user', to_field='employee_number'),
            preserve_default=False,
        ),
    ]
