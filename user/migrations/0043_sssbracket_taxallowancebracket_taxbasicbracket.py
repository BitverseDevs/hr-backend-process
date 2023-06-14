# Generated by Django 4.2 on 2023-06-14 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0042_alter_allowanceentry_table_alter_allowancetype_table_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SSSBracket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ramount_from', models.FloatField()),
                ('ramount_to', models.FloatField()),
                ('amount_rate', models.FloatField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'TBL_SSS_BRACKET',
            },
        ),
        migrations.CreateModel(
            name='TaxAllowanceBracket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ramount_from', models.FloatField()),
                ('ramount_to', models.FloatField()),
                ('amount_rate', models.FloatField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'TBL_ALLOWA_BRACKET',
            },
        ),
        migrations.CreateModel(
            name='TaxBasicBracket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ramount_from', models.FloatField()),
                ('ramount_to', models.FloatField()),
                ('amount_rate', models.FloatField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_deleted', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'TBL_TAX_BASIC_BRACKET',
            },
        ),
    ]