# Generated by Django 4.2 on 2023-04-27 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_employee_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='city_code',
            field=models.PositiveSmallIntegerField(default=1, verbose_name=((1, 'Caloocan'), (2, 'Las Piñas'), (3, 'Makati'), (4, 'Malabon'), (5, 'Mandaluyong'), (6, 'Manila'), (7, 'Marikina'), (8, 'Muntinlupa'), (9, 'Navotas'), (10, 'Parañaque'), (11, 'Pasay'), (12, 'Pasig'), (13, 'Paterso'), (14, 'Quezon City'), (15, 'San Juan'), (16, 'Taguig'), (17, 'Valenzuela'))),
        ),
        migrations.AlterField(
            model_name='employee',
            name='department_code',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Administration'), (2, 'Accounting Department'), (3, 'IT Department'), (4, 'HR Department')], default=1),
        ),
        migrations.AlterField(
            model_name='employee',
            name='division_code',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Administration'), (2, 'Accounting Department'), (3, 'IT Department'), (4, 'HR Department')], default=1),
        ),
        migrations.AlterField(
            model_name='employee',
            name='payroll_group_code',
            field=models.PositiveSmallIntegerField(choices=[(1, '20'), (2, '25'), (3, '30')], default=1),
        ),
        migrations.AlterField(
            model_name='employee',
            name='philhealth_code',
            field=models.PositiveSmallIntegerField(choices=[(1, '30%'), (2, '50%'), (3, '70%')], default=1),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position_code',
            field=models.PositiveSmallIntegerField(choices=[(1, 'President'), (2, 'Vice President'), (3, 'Manager'), (4, 'Supervisor'), (5, 'Sales Representative'), (6, 'Customer Service Representative'), (7, 'Marketing Coordinator'), (8, 'Human Resource Coordinator'), (9, 'Accountant'), (10, 'Administrative Assistant'), (11, 'IT Specialist'), (12, 'Graphic Designer'), (13, 'Operations Manager'), (14, 'Project Manager'), (15, 'Production Coordinator'), (16, 'Quality Assurance Specialist'), (17, 'Procurement Specialist'), (18, 'Logistics Coordinator'), (19, 'Business Development Manager'), (20, 'Legal Counsel')], default=1),
        ),
        migrations.AlterField(
            model_name='employee',
            name='rank_code',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Junior Level'), (2, 'Mid Level'), (3, 'Senior Level')], default=1),
        ),
        migrations.AlterField(
            model_name='employee',
            name='sssid_code',
            field=models.PositiveSmallIntegerField(choices=[(1, '30%'), (2, '50%'), (3, '70%')], default=1),
        ),
        migrations.AlterField(
            model_name='employee',
            name='tax_code',
            field=models.PositiveSmallIntegerField(choices=[(1, '0%'), (2, '15%'), (3, '20%')], default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'employee'), (2, 'hr_staff'), (3, 'hr_admin'), (4, 'hr_superadmin'), (5, 'developer')], default=1),
        ),
    ]
