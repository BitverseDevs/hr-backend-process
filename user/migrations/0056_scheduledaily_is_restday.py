# Generated by Django 4.2 on 2023-07-03 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0055_bonuslist_dtrcutoff_rd_ot_total_hours_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledaily',
            name='is_restday',
            field=models.BooleanField(default=False),
        ),
    ]
