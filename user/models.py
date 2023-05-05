from django.db import models

from django.core.validators import MaxValueValidator

# from .choices import *
import secret
import datetime


"""
unique
validators
max length
null
blank
choices
default
"""



class Employee(models.Model):
    employee_number = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(9990)])
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25)
    suffix = models.CharField(max_length=4, null=True, blank=True) # choice
    birthday = models.DateField()
    birth_place = models.CharField(max_length=50, null=True, blank=True)
    civil_status = models.PositiveSmallIntegerField(default=1) # choice
    gender = models.CharField(max_length=1) # choice
    address = models.TextField(max_length=50)
    provincial_address = models.TextField(max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(max_length=15)
    email = models.EmailField()
    
    date_hired = models.DateField()
    date_resigned = models.DateField(null=True, blank=True)
    approver = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    date_added = models.DateField(auto_now_add=True)
    date_deleted = models.DateField(null=True, blank=True)

    branch_code = models.CharField(max_length=15, default="main") # choice
    department_code = models.PositiveSmallIntegerField(null=True, blank=True) #choice
    division_code = models.PositiveSmallIntegerField(null=True, blank=True) #choice
    payroll_group_code = models.PositiveSmallIntegerField(null=True, blank=True) #choice
    position_code = models.PositiveSmallIntegerField(null=True, blank=True) #choice
    rank_code = models.PositiveSmallIntegerField(null=True, blank=True) #choice
    tax_code = models.PositiveSmallIntegerField(null=True, blank=True) #choice
    city_code = models.PositiveSmallIntegerField(null=True, blank=True) #choice
    
    pagibig_code = models.PositiveSmallIntegerField(null=True, blank=True)
    sssid_code = models.PositiveSmallIntegerField(null=True, blank=True)
    philhealth_code = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "TBL_EMPLOYEE_PROFILE"

class User(models.Model):
    employee_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    username = models.CharField(unique=True, max_length=8)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField() # choice

    is_active = models.BooleanField(default=1)
    is_locked = models.BooleanField(default=0)
    
    date_added = models.DateField(auto_now_add=True)
    date_deleted = models.DateField(null=True, blank=True)

    failed_login_attempts = models.PositiveSmallIntegerField(null=True, blank=True)
    last_login = models.DateTimeField(default=datetime.datetime(2023, 1, 1))

    old_password = models.CharField(max_length=128, default="")
    date_password_changed = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "TBL_USER"

class AuditTrail(models.Model):
    employee_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    transaction_type = models.CharField(max_length=15) # choice
    table_affected = models.CharField(max_length=30)
    action_remarks = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "TBL_AUDITTRAIL"

class DTR(models.Model):
    employe_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    bio_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    datetime_bio = models.DateTimeField()
    
    flag1_in_out = models.BooleanField() # choice
    flag2_lout_lin = models.BooleanField(null=True, blank=True) # choice
    entry_type = models.CharField(max_length=5) # choice
    date_uploaded = models.DateTimeField()
    processed = models.BooleanField(default=False)

    sched_timein = models.DateTimeField()
    sched_timeout = models.DateTimeField()
    business_datetime = models.DateTimeField()
    branch_code = models.CharField(max_length=15, default="main") # choice

    class Meta:
        db_table = "TBL_DTR"

class DTRSummary(models.Model):
    employee_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    cutoff_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    business_datetime = models.DateTimeField()
    shift_name = models.CharField(max_length=10) # choice
    date_in = models.DateTimeField()
    date_out = models.DateTimeField()
    
    sched_timein = models.DateTimeField()
    sched_timeout = models.DateTimeField()
    sched_restday = models.BooleanField()
    lunch_out = models.DateTimeField()
    lunch_in = models.DateTimeField()
    overbreak = models.PositiveSmallIntegerField()
    lates = models.PositiveSmallIntegerField()
    adjusted_timein = models.DateTimeField()
    adjusted_timeout = models.DateTimeField()
    
    total_hours = models.PositiveSmallIntegerField()
    paid_leave = models.BooleanField(default=False)
    paid_leave_reason = models.CharField(max_length=50) # choice
    reg_ot_total = models.PositiveSmallIntegerField()
    nd_ot_total = models.PositiveSmallIntegerField()
    ot_approved = models.BooleanField(default=False)
    pay_period = models.DateTimeField()
    is_computed = models.BooleanField(default=False)

    class Meta:
        bd_table = "TBL_DTR_SUMMARY"

class Holiday(models.Model):
    holiday_date = models.DateField()
    holiday_description = models.TextField(max_length=100)
    holiday_type = models.CharField(max_length=15) # choice
    holiday_location = models.CharField(max_length=15) # choice

    class Meta:
        db_table = "TBL_HOLIDAY"

class OBT(models.Model):
    employee_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    cutoff_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    
    obt_date_filed = models.DateTimeField(auto_now_add=True)
    obt_type = models.CharField(max_length=20) # choice
    obt_location = models.TextField(max_length=50)
    obt_remarks = models.TextField(max_length=100)
    obt_date_from = models.DateTimeField()
    obt_date_to = models.DateTimeField()
    obt_approval_status = models.CharField(max_length=3) # choice
    obt_reason_disapproval = models.TextField(max_length=50, null=True, blank=True)
    obt_total_hour = models.PositiveSmallIntegerField()
    obt_date_approved1 = models.DateTimeField(null=True, blank=True)
    obt_date_approved2 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_OBT_APP"

class Province(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "TBL_PROVINCE"

class CityMunicipality(models.Model):
    name = models.CharField(max_length=40)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        db_table = "TBL_CITYMUNICIPALITY"

class Overtime(models.Model):
    employee_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    cutoff_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    
    ot_date_filed = models.DateTimeField(auto_now_add=True)
    ot_type = models.CharField(max_length=2) # choice
    ot_remarks = models.TextField(max_length=100)
    ot_date_from = models.DateTimeField()
    ot_date_to = models.DateTimeField()
    ot_approval_status = models.PositiveSmallIntegerField() # choice
    ot_reason_disapproval = models.TextField(max_length=100)
    ot_total_hours = models.PositiveSmallIntegerField()
    ot_date_approved1 = models.DateTimeField(null=True, blank=True)
    ot_date_approved2 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_OVERTIME_APP"

class Leaves(models.Model):
    employee_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    cutoff_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    
    leave_date_filed = models.DateTimeField(auto_now_add=True)
    leave_type = models.CharField(max_length=3) # choice
    leave_remarks = models.TextField(max_length=100)
    leave_date_from = models.DateTimeField()
    leave_date_to = models.DateTimeField()
    leave_approval_status = models.CharField(max_length=3) # choice
    leave_reason_disapproval = models.TextField(max_length=100)
    leave_total_hours = models.PositiveSmallIntegerField()
    leave_date_approved1 = models.DateTimeField(null=True, blank=True)
    leave_date_approved2 = models.DateTimeField(null=True, blank=True)
    leave_number_days = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "TBL_LEAVES_APP"





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
