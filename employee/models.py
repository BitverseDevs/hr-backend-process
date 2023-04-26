from django.db import models
from user.models import User
from .choices import *

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
