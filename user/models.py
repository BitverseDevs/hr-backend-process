from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser

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

SUFFIX = [
    ("sr", "Sr."),
    ("jr", "Jr."),
    ("iii", "III/Third"),
    ("iv", "IV/Fourth"),
    ("v", "V/Fifth"),
]

GENDER = [
    ("m", "Male"),
    ("f", "Femals"),
]

CIVIL_STATUS = [
    (1, "Single"),
    (2, "Married"),
    (3, "Annulled"),
    (4, "Widowed"),
    (5, "Separated"),
]

ENTRY_TYPE = [
    ("din", "Duty In"),
    ("dout", "Duty Out"),
    ("lout", "Lunch Out"),
    ("lin", "Lunch In"),
]

SHIFT = [
    ("morning", "Morning Shift"),
    ("mid", "Mid Shift"),
    ("night", "Night Shift"),
]

HOLIDAY_TYPE = [
    ("sh", "Special Non-working Holiday"),
    ("lh", "Legal Working Holiday"),
]

HOLIDAY_LOCATION = [
    ("city", "City"),
    ("province", "Province"),
    ("national", "National"),
]

APPROVAL_STATUS = [
    ("p1", "Pending"),
    ("p2", "Pending2"),
    ("apd", "Approved"),
    ("dis", "Disapproved"),
]

OT_TYPE = [
    ("wd", "Whole Day Overtime"),
    ("bd", "Before Duty-in"),
    ("ad", "After Duty-in"),
]

class Branch(models.Model):
    name = models.CharField(max_length=25)
    address = models.TextField(max_length=50)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    oic = models.CharField(max_length=25)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_BRANCH"

class Department(models.Model):
    name = models.CharField(max_length=25)
    lead = models.CharField(max_length=25)
    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_DEPARTMENT"

class Division(models.Model):
    name = models.CharField(max_length=25)
    lead = models.CharField(max_length=25)
    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_DIVISION"

class Rank(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=100)
    is_approver = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_RANK"

class Position(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_POSITION"

class Province(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "TBL_PROVINCE"

class CityMunicipality(models.Model):
    name = models.CharField(max_length=40)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        db_table = "TBL_CITYMUNICIPALITY"

class Employee(models.Model):
    employee_number = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(9990)])
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25)
    suffix = models.CharField(max_length=4, null=True, blank=True, choices=SUFFIX)
    birthday = models.DateField()
    birth_place = models.CharField(max_length=50, null=True, blank=True)
    civil_status = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)], default=1, choices=CIVIL_STATUS)
    gender = models.CharField(max_length=1, choices=GENDER)
    address = models.TextField(max_length=50)
    provincial_address = models.TextField(max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(max_length=15)
    email = models.EmailField()
    
    date_hired = models.DateField()
    date_resigned = models.DateField(null=True, blank=True)
    approver = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    date_added = models.DateField(auto_now_add=True)
    date_deleted = models.DateField(null=True, blank=True)

    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    department_code = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    division_code = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    payroll_group_code = models.PositiveSmallIntegerField(null=True, blank=True) #choice
    position_code = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    rank_code = models.ForeignKey(Rank, on_delete=models.CASCADE, null=True, blank=True)
    tax_code = models.PositiveSmallIntegerField(null=True, blank=True) #choice
    city_code = models.ForeignKey(CityMunicipality, on_delete=models.CASCADE, null=True, blank=True)
    
    pagibig_code = models.PositiveSmallIntegerField(null=True, blank=True)
    sssid_code = models.PositiveSmallIntegerField(null=True, blank=True)
    philhealth_code = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        db_table = "TBL_EMPLOYEE_PROFILE"

class User(AbstractUser):
    employee_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    username = models.CharField(unique=True, max_length=8)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField() # choice

    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)
    
    date_added = models.DateField(auto_now_add=True)
    date_deleted = models.DateField(null=True, blank=True)

    failed_login_attempts = models.PositiveSmallIntegerField(null=True, blank=True)
    last_login = models.DateTimeField(default=datetime.datetime(2023, 1, 1))

    old_password = models.CharField(max_length=128, default="N/A")
    date_password_changed = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", "role", "is_active", "is_locked"]

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
    employee_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    bio_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    datetime_bio = models.DateTimeField()
    
    flag1_in_out = models.BooleanField() # 0:DutyIn; 1:DutyOut
    flag2_lout_lin = models.BooleanField(null=True, blank=True) # 0:Lunchin; 1:LunchOut 
    entry_type = models.CharField(max_length=4, choices=ENTRY_TYPE)
    date_uploaded = models.DateTimeField()
    processed = models.BooleanField(default=False)

    sched_timein = models.DateTimeField()
    sched_timeout = models.DateTimeField()
    business_datetime = models.DateTimeField()
    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE)

    class Meta:
        db_table = "TBL_DTR"

class DTRSummary(models.Model):
    employee_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    cutoff_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    business_datetime = models.DateTimeField()
    shift_name = models.CharField(max_length=10, choices=SHIFT)
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
        db_table = "TBL_DTR_SUMMARY"

class Holiday(models.Model):
    holiday_date = models.DateField()
    holiday_description = models.TextField(max_length=100)
    holiday_type = models.CharField(unique=True, max_length=5, choices=HOLIDAY_TYPE)
    holiday_location = models.CharField(max_length=15, choices=HOLIDAY_LOCATION) 

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
    obt_approval_status = models.CharField(max_length=3, choices=APPROVAL_STATUS)
    obt_reason_disapproval = models.TextField(max_length=50, null=True, blank=True)
    obt_total_hour = models.PositiveSmallIntegerField()
    obt_date_approved1 = models.DateTimeField(null=True, blank=True)
    obt_date_approved2 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_OBT_APP"

class Overtime(models.Model):
    employee_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    cutoff_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    
    ot_date_filed = models.DateTimeField(auto_now_add=True)
    ot_type = models.CharField(max_length=2, choices=OT_TYPE)
    ot_remarks = models.TextField(max_length=100)
    ot_date_from = models.DateTimeField()
    ot_date_to = models.DateTimeField()
    ot_approval_status = models.CharField(max_length=3, choices=APPROVAL_STATUS)
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
    leave_approval_status = models.CharField(max_length=3, choices=APPROVAL_STATUS)
    leave_reason_disapproval = models.TextField(max_length=100, null=True, blank=True)
    leave_total_hours = models.PositiveSmallIntegerField()
    leave_date_approved1 = models.DateTimeField(null=True, blank=True)
    leave_date_approved2 = models.DateTimeField(null=True, blank=True)
    leave_number_days = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "TBL_LEAVES_APP"

class Adjustment(models.Model):
    employee_number = models.ForeignKey(Employee, to_field="employee_number", on_delete=models.CASCADE)
    cutoff_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    deducted_amount = models.FloatField()
    added_amount = models.FloatField()
    adjustment_remark = models.TextField(max_length=100)
    adjustment_remark2 = models.TextField(max_length=100)
    prepared_by_employee_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    approved_by_employee_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    is_computed = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_ADJUSTMENT_ENTRY"