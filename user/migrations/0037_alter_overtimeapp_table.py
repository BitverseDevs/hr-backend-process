# Generated by Django 4.2 on 2023-05-04 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0036_rename_overtimeentry_overtimeapp_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='overtimeapp',
            table='TBL_OVERTIME',
        ),
    ]
