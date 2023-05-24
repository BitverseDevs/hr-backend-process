from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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

PAYROLL_FREQUENCY = (
    (1, "Monthly"),
    (2, "Semi-Monthly"),
    (3, "Project-Based"),
    (4, "Weekly"),
)

TAX_FREQUENCY = (
    (1, "Semi-Monthly"),
    (2, "Monthly"),
    (3, "Annual"),
)

SUFFIX = [
    ("sr", "Sr."),
    ("jr", "Jr."),
    ("iii", "III/Third"),
    ("iv", "IV/Fourth"),
    ("v", "V/Fifth"),
]

GENDER = [
    ("M", "Male"),
    ("F", "Female"),
]

CIVIL_STATUS = [
    ("S", "Single"),
    ("M", "Married"),
    ("A", "Annulled"),
    ("W", "Widowed"),
    ("SE", "Separated"),
]

HOLIDAY_TYPE = [
    ("SH", "Special Non-working Holiday"),
    ("LH", "Legal Working Holiday"),
]

HOLIDAY_LOCATION = [
    ("city", "City"),
    ("province", "Province"),
    ("national", "National"),
]

APPROVAL_STATUS = [
    ("P1", "Pending"),
    ("P2", "Pending2"),
    ("APD", "Approved"),
    ("DIS", "Disapproved"),
]

OT_TYPE = [
    ("WD", "Whole Day Overtime"),
    ("BD", "Before Duty-in"),
    ("AD", "After Duty-in"),
]

def upload_to(instance, filename):
    return f'image/{filename}'

class Branch(models.Model):
    branch_name = models.CharField(max_length=25)
    branch_address = models.TextField(max_length=50)
    branch_email = models.EmailField()
    branch_contact_number = models.CharField(max_length=15)
    branch_oic = models.CharField(max_length=25)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_BRANCH_CODE"

class Department(models.Model):
    dept_name = models.CharField(max_length=25)
    dept_lead = models.ForeignKey("Employee", to_field="emp_no", on_delete=models.CASCADE)
    dept_branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE, default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_DEPARTMENT_CODE"

class Division(models.Model):
    div_name = models.CharField(max_length=25)
    div_lead = models.ForeignKey("Employee", to_field="emp_no", on_delete=models.CASCADE)
    div_branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_DIVISION_CODE"

class PayrollGroup(models.Model):
    name = models.CharField(max_length=25)
    payroll_description = models.TextField(max_length=75, null=True, blank=True)
    payroll_freq = models.PositiveSmallIntegerField(validators=[MaxValueValidator(4)], choices=PAYROLL_FREQUENCY)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)
    used_account =models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "TBL_PAYROLL_GROUP_CODE"

class Position(models.Model):
    pos_name = models.CharField(max_length=25)
    pos_description = models.TextField(max_length=75, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_POSITION_CODE"

class Rank(models.Model):
    rank_name = models.CharField(max_length=25)
    rank_description = models.TextField(max_length=75, null=True, blank=True)
    is_approver = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_RANK_CODE"

class Tax(models.Model):
    emp_no = models.ForeignKey("Employee", to_field="emp_no", on_delete=models.CASCADE)
    tin_no = models.CharField(max_length=12)
    tax_form = models.CharField(max_length=15, null=True, blank=True)
    tax_description = models.TextField(max_length=75, null=True, blank=True)
    tax_percentage = models.FloatField(null=True, blank=True)
    tax_amount = models.FloatField(null=True, blank=True)
    payment_frequency = models.PositiveSmallIntegerField(validators=[MaxValueValidator(4)], choices=TAX_FREQUENCY, null=True, blank=True)

    class Meta:
        db_table = "TBL_TAX_CODE"

class Province(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "TBL_PROVINCE"

class CityMunicipality(models.Model):
    name = models.CharField(max_length=50)
    province_code = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        db_table = "TBL_CITYMUNICIPALITY"

class PAGIBIG(models.Model):
    emp_no = models.ForeignKey("Employee", to_field="emp_no", on_delete=models.CASCADE)
    pagibig_no = models.CharField(max_length=15)
    pagibig_contribution_month = models.FloatField(null=True, blank=True)
    pagibig_with_cloan_amount = models.FloatField(null=True, blank=True)
    pagibig_rem_cloan_amount = models.FloatField(null=True, blank=True)
    pagibig_with_hloan_amount = models.FloatField(null=True, blank=True)
    pagibig_rem_hloan_amount = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "TBL_PAGIBIG_CODE"

class SSS(models.Model):
    emp_no = models.ForeignKey("Employee", to_field="emp_no", on_delete=models.CASCADE)
    sss_number = models.CharField(max_length=10)
    sss_contribution_month = models.FloatField(null=True, blank=True)
    sss_with_cashloan_amount = models.FloatField(null=True, blank=True)
    sss_rem_cashloan_amount = models.FloatField(null=True, blank=True)
    sss_with_calloan_amount = models.FloatField(null=True, blank=True)
    sss_rem_callloan_amount = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "TBL_SSS_CODE"
    
class Philhealth(models.Model):
    emp_no = models.ForeignKey("Employee", to_field="emp_no", on_delete=models.CASCADE)
    ph_no = models.CharField(max_length=10)
    ph_contribution_month = models.FloatField(null=True, blank=True)
    ph_category = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = "TBL_PHILHEALTH_CODE"

class Employee(models.Model):
    emp_no = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(9990)])
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25)
    suffix = models.CharField(max_length=4, null=True, blank=True, choices=SUFFIX)
    birthday = models.DateField()
    birth_place = models.CharField(max_length=50, null=True, blank=True)
    civil_status = models.CharField(max_length=2, choices=CIVIL_STATUS)
    gender = models.CharField(max_length=1, choices=GENDER)
    address = models.TextField(max_length=50)
    provincial_address = models.TextField(max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(max_length=15)
    email_address = models.EmailField()
    employee_image = models.ImageField(_("Image"), upload_to=upload_to, null=True, blank=True)
    bio_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)], null=True, blank=True, unique=True)
    
    date_hired = models.DateField()
    date_resigned = models.DateField(null=True, blank=True)
    approver = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    date_added = models.DateField(auto_now_add=True)
    date_deleted = models.DateField(null=True, blank=True)

    city_code = models.ForeignKey(CityMunicipality, on_delete=models.CASCADE, null=True, blank=True)
    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    department_code = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    division_code = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)    
    position_code = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    rank_code = models.ForeignKey(Rank, on_delete=models.CASCADE, null=True, blank=True)
    
    payroll_group_code = models.ForeignKey(PayrollGroup, on_delete=models.CASCADE, null=True, blank=True)
    tax_code = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True)
    pagibig_code = models.ForeignKey(PAGIBIG, on_delete=models.CASCADE, null=True, blank=True)
    sssid_code = models.ForeignKey(SSS, on_delete=models.CASCADE, null=True, blank=True)
    philhealth_code = models.ForeignKey(Philhealth, on_delete=models.CASCADE, null=True, blank=True)

    def days_before(self, date):
        today = datetime.date.today()
        next_day = datetime.date(today.year, date.month, date.day)
        if next_day.month < today.month or next_day.day < today.day:
            next_day = next_day.replace(year=today.year + 1)
        days = next_day - today

        return (days.days + datetime.time(days=1)) if (today.year%4 == 0) else days.days

    class Meta:
        db_table = "TBL_EMPLOYEE_PROFILE"

class User(AbstractUser):
    emp_no = models.OneToOneField(Employee, to_field="emp_no", on_delete=models.CASCADE)
    username = models.CharField(unique=True, max_length=8)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField() # choice
    is_active = models.BooleanField(default=True)

    is_logged_in = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    last_login = models.DateTimeField(default=datetime.datetime(2023, 1, 1))
    old_password = models.CharField(max_length=128, default="N/A")
    date_password_changed = models.DateField(null=True, blank=True)
    
    date_added = models.DateField(auto_now_add=True)
    date_deleted = models.DateField(null=True, blank=True)

    #  To remove default fields of Django User Model

    first_name = None
    last_name = None
    email = None
    is_staff = None
    date_joined = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", "role", "is_active"]

    class Meta:
        db_table = "TBL_USER"

class AuditTrail(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=15) # choice
    table_affected = models.CharField(max_length=30)
    action_remarks = models.TextField(max_length=75)

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "TBL_AUDITTRAIL"

class DTR(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE, null=True, blank=True)
    bio_id = models.ForeignKey(Employee, to_field="bio_id", on_delete=models.CASCADE, related_name="dtrbio_id")
    branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    datetime_bio = models.DateTimeField()
    
    flag1_in_out = models.BooleanField() # 0:DutyIn; 1:DutyOut
    flag2_lout_lin = models.BooleanField(null=True, blank=True) # 0:LunchIn; 1:LunchOut
    entry_type = models.CharField(max_length=4, null=True, blank=True)
    schedule_daily_code = models.ForeignKey("ScheduleDaily", on_delete=models.CASCADE)
    
    date_uploaded = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        db_table = "TBL_DTR_ENTRY"

class DTRSummary(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    cutoff_code = models.ForeignKey("Cutoff", on_delete=models.CASCADE)
    business_date = models.DateField()
    shift_name = models.CharField(max_length=25)
    duty_in = models.DateTimeField()
    duty_out = models.DateTimeField()
    
    sched_timein = models.DateTimeField()
    sched_timeout = models.DateTimeField()
    is_sched_restday = models.BooleanField()
    lunch_out = models.DateTimeField(null=True, blank=True)
    lunch_in = models.DateTimeField(null=True, blank=True)
    overbreak = models.PositiveSmallIntegerField(null=True, blank=True)
    lates = models.PositiveSmallIntegerField()
    adjusted_timein = models.DateTimeField(null=True, blank=True)
    adjusted_timeout = models.DateTimeField(null=True, blank=True)
    
    total_hours = models.PositiveSmallIntegerField()
    is_paid_leave = models.BooleanField(default=False)
    paid_leave_type = models.CharField(max_length=50) # choice
    reg_ot_total = models.PositiveSmallIntegerField()
    nd_ot_total = models.PositiveSmallIntegerField()
    is_obt = models.BooleanField(default=False)
    is_sp_holiday = models.BooleanField(default=False)
    is_reg_holiday = models.BooleanField(default=False)
    is_absent = models.BooleanField(default=False)
    is_computed = models.BooleanField(default=False)

    class Meta:
        db_table = "TBL_DTR_SUMMARY"

class DTRCutoff(models.Model):
    cutoff_code = models.ForeignKey("Cutoff", on_delete=models.CASCADE)
    emp_no = models.ForeignKey(Employee, on_delete=models.CASCADE)
    business_date_from = models.DateField()
    business_date_to = models.DateField()
    hours_total = models.PositiveSmallIntegerField()
    overbreak_total = models.PositiveSmallIntegerField(null=True, blank=True)
    lates_total = models.PositiveSmallIntegerField(null=True, blank=True)
    paid_leaves_total = models.PositiveSmallIntegerField(null=True, blank=True)
    reg_ot_total = models.PositiveSmallIntegerField(null=True, blank=True)
    nd_ot_total = models.PositiveSmallIntegerField(null=True, blank=True)
    sp_holiday_total = models.PositiveSmallIntegerField(null=True, blank=True)
    reg_holiday_total = models.PositiveSmallIntegerField(null=True, blank=True)
    absent_total = models.PositiveSmallIntegerField(null=True, blank=True)
    leaves_type_used = models.CharField(max_length=40, null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_DTR_CUTOFF_SUMMARY"

class Holiday(models.Model):
    holiday_date = models.DateField()
    holiday_description = models.TextField(max_length=75, null=True, blank=True)
    holiday_type = models.CharField(unique=True, max_length=5, choices=HOLIDAY_TYPE)
    holiday_location = models.CharField(max_length=15, choices=HOLIDAY_LOCATION) 

    class Meta:
        db_table = "TBL_HOLIDAY_TYPE"

class OBT(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    cutoff_code = models.ForeignKey("Cutoff", on_delete=models.CASCADE)
    
    obt_date_filed = models.DateTimeField(auto_now_add=True)
    obt_type = models.CharField(max_length=20) # choice
    obt_location = models.TextField(max_length=50)
    obt_remarks = models.TextField(max_length=75)
    obt_date_from = models.DateTimeField()
    obt_date_to = models.DateTimeField()
    obt_approval_status = models.CharField(max_length=3, choices=APPROVAL_STATUS)
    obt_reason_disapproval = models.TextField(max_length=50, null=True, blank=True)
    obt_total_hour = models.PositiveSmallIntegerField()
    obt_approver1_empno = models.PositiveSmallIntegerField()
    obt_date_approved1 = models.DateTimeField()
    obt_approver2_empono = models.PositiveSmallIntegerField(null=True, blank=True)
    obt_date_approved2 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_OBT_APP"

class Overtime(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    cutoff_code = models.ForeignKey("Cutoff", on_delete=models.CASCADE)
    
    ot_date_filed = models.DateTimeField(auto_now_add=True)
    ot_type = models.CharField(max_length=2, choices=OT_TYPE)
    ot_remarks = models.TextField(max_length=75)
    ot_date_from = models.DateTimeField()
    ot_date_to = models.DateTimeField()
    ot_approval_status = models.CharField(max_length=3, choices=APPROVAL_STATUS)
    ot_reason_disapproval = models.TextField(max_length=100)
    ot_total_hours = models.PositiveSmallIntegerField()
    ot_approver1_empno = models.PositiveSmallIntegerField()
    ot_date_approved1 = models.DateTimeField(null=True, blank=True)
    ot_approver2_empno = models.PositiveSmallIntegerField(null=True, blank=True)
    ot_date_approved2 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_OVERTIME_APP"

class Leaves(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    cutoff_code = models.ForeignKey("Cutoff", on_delete=models.CASCADE)
    
    leave_date_filed = models.DateTimeField(auto_now_add=True)
    leave_type = models.ForeignKey("LeavesType", on_delete=models.CASCADE)
    leave_remarks = models.TextField(max_length=75)
    leave_date_from = models.DateTimeField()
    leave_date_to = models.DateTimeField()
    leave_approval_status = models.CharField(max_length=3, choices=APPROVAL_STATUS)
    leave_reason_disapproval = models.TextField(max_length=100, null=True, blank=True)
    leave_total_hours = models.PositiveSmallIntegerField()
    leave_approver1_empno = models.PositiveSmallIntegerField()
    leave_date_approved1 = models.DateTimeField(null=True, blank=True)
    leave_approver2_empno = models.PositiveSmallIntegerField(null=True, blank=True)
    leave_date_approved2 = models.DateTimeField(null=True, blank=True)
    leave_number_days = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "TBL_LEAVES_APP"

class LeavesCredit(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    leave_type_code = models.ForeignKey("LeavesType", on_delete=models.CASCADE)
    allowed_days = models.DateTimeField(null=True, blank=True)
    credit_used = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)], null=True, blank=True)
    credit_remaining = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)], null=True, blank=True)
    expiry = models.DateTimeField()
    is_converted = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_LEAVES_CREDIT"

class LeavesType(models.Model):
    name = models.CharField(max_length=25)
    date_added = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_LEAVES_TYPE"

class Adjustment(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    cutoff_code = models.ForeignKey("Cutoff", on_delete=models.CASCADE)
    deducted_amount = models.FloatField()
    added_amount = models.FloatField()
    adjustment_remark = models.TextField(max_length=100)
    adjustment_remark2 = models.TextField(max_length=100)
    prepared_by_empno = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    approved_by_empno = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)])
    is_computed = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_ADJUSTMENT_ENTRY"

class Cutoff(models.Model):
    co_name = models.CharField(max_length=25)
    co_description = models.TextField(max_length=75)
    co_date_from = models.DateTimeField()
    co_date_to = models.DateTimeField()
    payroll_group_code = models.ForeignKey(PayrollGroup, on_delete=models.CASCADE)
    division_code = models.ForeignKey(Division, on_delete=models.CASCADE)
    co_is_processed = models.BooleanField()
    credit_date = models.DateTimeField()

    class Meta:
        db_table = "TBL_CUTOFF_PERIOD_LIST"

class ScheduleShift(models.Model):
    name = models.CharField(max_length=25)
    time_in = models.TimeField()
    time_out = models.TimeField()
    grace_period = models.PositiveSmallIntegerField(null=True, blank=True)
    with_overtime = models.BooleanField()
    is_night_shift = models.BooleanField()
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_SCHEDULE_SHIFT"

class ScheduleDaily(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    business_date = models.DateField()
    schedule_shift_code = models.ForeignKey(ScheduleShift, on_delete=models.CASCADE)
    is_processed = models.BooleanField(null=True, blank=True)
    sched_default = models.ForeignKey(ScheduleShift, on_delete=models.CASCADE, null=True, blank=True, related_name="sched_daily_default")

    class Meta:
        db_table = "TBL_SCHED_DAILY"

class UnaccountedAttendance(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    cutoff_code = models.ForeignKey(Cutoff, on_delete=models.CASCADE)
    ua_date_filed = models.DateTimeField(auto_now_add=True)
    ua_description = models.TextField(max_length=75)
    ua_date_from = models.DateTimeField()
    ua_date_to = models.DateTimeField()
    ua_approved_status = models.CharField(max_length=3, choices=APPROVAL_STATUS)
    ua_reason_disapproval = models.TextField(max_length=75, null=True, blank=True)
    ua_total_hour = models.PositiveSmallIntegerField()
    ua_approver1_empno = models.PositiveSmallIntegerField()
    ua_date_approved1 = models.DateTimeField(null=True, blank=True)
    ua_approver2_empno = models.PositiveSmallIntegerField(null=True, blank=True)
    ua_date_approved2 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_UNACCOUNTED_ATT"