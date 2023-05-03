import datetime
from django.db import models
from django.core.validators import MaxValueValidator
import secret
from .choices import *

# Constants
EMPLOYEE_NUMBER_MAX = 9990
USERNAME_LENGTH_MAX = 8

class User(models.Model):
    
    employee_number = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(EMPLOYEE_NUMBER_MAX)])
    username = models.CharField(max_length=USERNAME_LENGTH_MAX, unique=True)
    password = models.CharField(max_length=128)
    date_added = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    date_deleted = models.DateTimeField(blank=True, null=True)
    is_locked = models.BooleanField(default=False)

    failed_login_attempts = models.PositiveSmallIntegerField(null=True, blank=True)
    last_login = models.DateTimeField(default=datetime.datetime(2001, 1, 1))

    old_password = models.CharField(max_length=128, default=secret.DEF_PASS)
    date_password_change = models.DateTimeField(blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)
    

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'TBL_USER'



class Employee(models.Model):

    employee_number = models.ForeignKey(User, to_field='employee_number', on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25)
    suffix = models.CharField(max_length=4, null=True, blank=True, choices=SUFFIX)
    
    birthday = models.DateField()
    birth_place = models.CharField(max_length=25, null=True, blank=True)
    civil_status = models.PositiveSmallIntegerField(choices=CIVIL_STATUS, default=1)
    gender = models.CharField(max_length=1, choices=GENDER)
    
    address = models.CharField(max_length=50)
    provincial_address = models.CharField(max_length=50, null=True, blank=True)
    
    mobile_phone = models.CharField(max_length=15)
    email = models.EmailField()
    
    approver = models.CharField(max_length=4)
    
    date_hired = models.DateField()
    date_resigned = models.DateField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(blank=True, null=True)

    branch_code = models.CharField(max_length=15, choices=BRANCH, default="main")
    department_code = models.PositiveSmallIntegerField(choices=DEPT, null=True, blank=True)
    division_code = models.PositiveSmallIntegerField(choices=DIV, null=True, blank=True)
    position_code = models.PositiveSmallIntegerField(choices=POS, null=True, blank=True)
    rank_code = models.PositiveSmallIntegerField(choices=RANK, null=True, blank=True)
    city_code = models.PositiveSmallIntegerField(choices=CITY, null=True, blank=True)

    payroll_group_code = models.PositiveSmallIntegerField(choices=PAYROLL, null=True, blank=True)
    tax_code = models.PositiveSmallIntegerField(choices=TAX, null=True, blank=True)
    pagibig_code = models.PositiveSmallIntegerField(choices=PAGIBIG, null=True, blank=True)
    sssid_code = models.PositiveSmallIntegerField(choices=SSS, null=True, blank=True)
    philhealth_code = models.PositiveSmallIntegerField(choices=PHILHEALTH, null=True, blank=True)



    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'TBL_EMPLOYEE_PROFILE'



class AuditTrail(models.Model):

    # transaction_id = models.AutoField(primary_key=True)
    employee_number = models.ForeignKey(User, to_field='employee_number', on_delete=models.CASCADE)
    transaction_type = models.PositiveSmallIntegerField(choices=TRANS_TYPE)
    table_affected = models.CharField(max_length=100)
    action_remarks = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.id}: {self.transaction_type}"

    class Meta:
        db_table = "TBL_AUDTRAIL"



class DTR(models.Model):

    bio_id = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(9990)], null=True, blank=True)
    date_time_bio = models.DateTimeField()
    flag1_in_out = models.BooleanField(choices=FLAG)
    flag2_lout_lin = models.BooleanField(choices=FLAG, null=True, blank=True)

    entry_type = models.CharField(max_length=4, choices=ENTRY)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    employee_number = models.ForeignKey(User, to_field='employee_number', on_delete=models.CASCADE)
    processed = models.BooleanField()
    
    sched_timein = models.DateTimeField()
    sched_timeout = models.DateTimeField()
    business_datetime = models.DateTimeField()
    branch_code =models.CharField(max_length=15, choices=BRANCH, default="main")



    class Meta:
        db_table = "TBL_DTR"



class DTRSummary(models.Model):

    cutoff_id = models.PositiveSmallIntegerField()
    business_datetime = models.DateTimeField()
    shift_time = models.CharField(max_length=7, choices=SHIFTS)
    date_in = models.DateTimeField()
    date_out = models.DateTimeField()
    employee_number = models.ForeignKey(User, to_field="employee_number", on_delete=models.CASCADE)
    sched_timein = models.DateTimeField()
    sched_timeout = models.DateTimeField()
    sched_restday = models.BooleanField()
    lunch_out = models.DateTimeField()
    lunch_in = models.DateTimeField()
    overbreak = models.PositiveSmallIntegerField()
    lates = models.PositiveSmallIntegerField()
    adjusted_time_in = models.DateTimeField()
    adjusted_time_out = models.DateTimeField()
    total_hours = models.PositiveSmallIntegerField()
    paid_leave = models.BooleanField(default=False)
    paid_leave_reason = models.CharField(max_length=15, choices=LEAVES, blank=True, null=True)
    reg_ot_total = models.PositiveSmallIntegerField()
    nd_ot_total = models.PositiveSmallIntegerField()
    ot_approved = models.BooleanField(default=False)
    pay_period = models.DateTimeField()
    is_computed = models.BooleanField(default=False)

    class Meta:
        db_table = "TBL_DTR_SUMMARY"



class CityMunicipality(models.Model):

    name = models.CharField(max_length=40)
    province = models.CharField(max_length=40)


    class Meta:
        db_table = "TBL_CITYMUNICIPALITY"


# class Branch(models.Model):

#     name = models.CharField(max_length=25)
#     address = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=15)
#     email = models.EmailField()
#     parent_branch = models.CharField(max_length=15, blank=True, null=True) # foreign to branch
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField()

# class Department(models.Model):

#     name = models.CharField(max_length=25)
#     description = models.TextField(max_length=100)
#     manager = models.CharField(max_length=25) # foreign to employee
#     parent_department = models.CharField(max_length=25, null=True, blank=True) # foreign to department
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField()

# class Division(models.Model):

#     name = models.CharField(max_length=25)
#     description = models.TextField(max_length=100)
#     manager = models.CharField(max_length=25) # foreign to employee
#     parent_department = models.CharField(max_length=25, null=True, blank=True) # foreign to department
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField()

# class PayrollGroup(models.Model):

#     name = models.CharField(max_length=15)
#     description = models.TextField(max_length=100)
#     pay_frequency = models.CharField(max_length=15, choices=FREQUENCY)
#     pay_day = models.PositiveSmallIntegerField()
#     is_default = models.BooleanField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField()

# class Position(models.Model):

#     title = models.CharField(max_length=25)
#     description = models.TextField(max_length=100)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     payroll_group = models.ForeignKey(PayrollGroup, on_delete=models.CASCADE)
#     minimum_qualifications = models.TextField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField()

# class Rank(models.Model):

#     name = models.CharField(max_length=25, choices=RANK)
#     description = models.TextField(max_length=100)
#     rate = models.DecimalField()
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField()
