# Generated by Django 4.2 on 2023-06-15 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0044_taxallowancebracket_frequency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taxallowancebracket',
            name='frequency',
        ),
        migrations.AddField(
            model_name='taxbasicbracket',
            name='frequency',
            field=models.CharField(default=1, max_length=1),
            preserve_default=False,
        ),
    ]
