# Generated by Django 4.2 on 2023-04-26 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_last_login_alter_user_username_alter_user_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='old_password',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]