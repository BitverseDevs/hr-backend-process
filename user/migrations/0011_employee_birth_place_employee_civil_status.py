# Generated by Django 4.2 on 2023-04-27 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_employee_city_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='birth_place',
            field=models.CharField(default='BATANES', max_length=25),
        ),
        migrations.AddField(
            model_name='employee',
            name='civil_status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Single'), (2, 'Married'), (3, 'Annulled'), (4, 'Widowed'), (5, 'Separated')], default=1),
        ),
    ]
