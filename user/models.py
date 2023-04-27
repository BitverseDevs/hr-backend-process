import datetime
from django.db import models
from django.core.validators import MaxValueValidator
import secret
from .choices import *

EMPLOYEE_ID_MAX = 9990
USERNAME_LENGTH_MAX = 8
ROLE_CHOICES = (
        (1, 'employee'),
        (2, 'hr_staff'),
        (3, 'hr_admin'),
        (4, 'hr_superadmin'),
        (5, 'developer'),
    )

class User(models.Model):
    
    employee_id = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(EMPLOYEE_ID_MAX)])
    username = models.CharField(max_length=USERNAME_LENGTH_MAX)
    password = models.CharField(max_length=128)
    date_added = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    date_deleted = models.DateTimeField(blank=True, null=True)
    is_locked = models.BooleanField(default=False)

    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    
    old_password = models.CharField(max_length=128, default=secret.DEF_PASS)
    date_password_change = models.DateTimeField(blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    last_login = models.DateTimeField(default=datetime.datetime(2001, 1, 1))

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'TBL_USER'



class Employee(models.Model):

    employee_id = models.ForeignKey(User, to_field='employee_id', on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25)
    suffix = models.CharField(max_length=4, null=True, blank=True)
    
    birthday = models.DateField()
    gender = models.BooleanField(choices=((0, 'Female'), (1, 'Male')))
    
    address = models.CharField(max_length=50)
    
    provincial_address = models.CharField(max_length=50, null=True, blank=True)
    
    mobile_phone = models.CharField(max_length=15)
    email = models.EmailField()
    
    approver = models.BooleanField(default=False)
    
    date_hired = models.DateField()
    date_resigned = models.DateField(null=True, blank=True)

    department_code = models.PositiveSmallIntegerField(choices=DEPT)
    division_code = models.PositiveSmallIntegerField(choices=DIV)
    position_code = models.PositiveSmallIntegerField(choices=POS)
    rank_code = models.PositiveSmallIntegerField(choices=RANK)
    city_code = models.PositiveSmallIntegerField(CITY)

    payroll_group_code = models.PositiveSmallIntegerField(choices=PAYROLL)
    tax_code = models.PositiveSmallIntegerField(choices=TAX)
    sssid_code = models.PositiveSmallIntegerField(choices=SSS)
    philhealth_code = models.PositiveSmallIntegerField(choices=PHILHEALTH)

    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(blank=True, null=True)



    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'TBL_EMPLOYEE_PROFILE'
    