from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import datetime



PAYROLL_FREQUENCY = (
    (1, "Monthly"),
    (2, "Semi-Monthly"),
    (3, "Project-Based"),
    (4, "Weekly"),
)

TAX_FREQUENCY = (
    (1, "Annual"),
    (2, "Monthly"),
    (3, "Semi-Monthly"),
)

HOLIDAY_TYPE = [
    ("SH", "Special Non-Working Holiday"),
    ("LH", "Legal Working Holiday"),
]

HOLIDAY_LOCATION = [
    ("City", "City"),
    ("Province", "Province"),
    ("National", "National"),
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
    hierarchy = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
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
    pagibig_with_calloan_amount = models.FloatField(null=True, blank=True)
    pagibig_rem_calloan_amount = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "TBL_PAGIBIG_CODE"

class SSS(models.Model):
    emp_no = models.ForeignKey("Employee", to_field="emp_no", on_delete=models.CASCADE)
    sss_no = models.CharField(max_length=10)
    sss_contribution_month = models.FloatField(null=True, blank=True)
    sss_with_cashloan_amount = models.FloatField(null=True, blank=True)
    sss_rem_cashloan_amount = models.FloatField(null=True, blank=True)
    sss_with_calloan_amount = models.FloatField(null=True, blank=True)
    sss_rem_calloan_amount = models.FloatField(null=True, blank=True)

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
    suffix = models.CharField(max_length=4, null=True, blank=True)
    birthday = models.DateField()
    birth_place = models.CharField(max_length=50, null=True, blank=True)
    civil_status = models.CharField(max_length=2)
    gender = models.CharField(max_length=1)
    address = models.TextField(max_length=50)
    provincial_address = models.TextField(max_length=50, null=True, blank=True)
    mobile_phone = models.CharField(max_length=15)
    email_address = models.EmailField()
    employee_image = models.ImageField(_("Image"), upload_to=upload_to, null=True, blank=True)
    bio_id = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)], null=True, blank=True, unique=True)
    
    date_hired = models.DateField()
    date_resigned = models.DateField(null=True, blank=True)
    approver = models.PositiveSmallIntegerField(validators=[MaxValueValidator(9990)], default=0)
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

    accnt_no = models.CharField(max_length=25, unique=True)
    emp_salary_basic = models.FloatField()
    # emp_salary_allowance = models.FloatField() # omitted
    # emp_salary_other = models.FloatField() # omitted
    emp_salary_type = models.CharField(max_length=7)

    insurance_life = models.FloatField(null=True, blank=True)
    other_deductible = models.FloatField(null=True, blank=True)
    ecola = models.FloatField(null=True, blank=True)

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
    shift_name = models.CharField(max_length=35, default="RD")
    duty_in = models.DateTimeField(null=True, blank=True)
    duty_out = models.DateTimeField(null=True, blank=True)
    
    sched_timein = models.TimeField(null=True, blank=True)
    sched_timeout = models.TimeField(null=True, blank=True)
    is_sched_restday = models.BooleanField(default=False)
    lunch_out = models.DateTimeField(null=True, blank=True)
    lunch_in = models.DateTimeField(null=True, blank=True)
    
    is_paid_leave = models.BooleanField(default=False)
    paid_leave_type = models.CharField(max_length=50, null=True, blank=True) # choice
    reg_ot_total = models.PositiveSmallIntegerField(default=0)
    nd_ot_total = models.PositiveSmallIntegerField(default=0)
    is_obt = models.BooleanField(default=False)
    is_sp_holiday = models.BooleanField(default=False)
    is_reg_holiday = models.BooleanField(default=False)
    is_ua = models.BooleanField(default=False)
    is_absent = models.BooleanField(default=False)

    overbreak = models.PositiveSmallIntegerField(null=True, blank=True)
    lates = models.PositiveSmallIntegerField()
    undertime = models.PositiveSmallIntegerField()
    total_hours = models.PositiveSmallIntegerField()
    nd_total_hours = models.PositiveSmallIntegerField(null=True, blank=True)

    adjusted_timein = models.DateTimeField(null=True, blank=True)
    adjusted_timeout = models.DateTimeField(null=True, blank=True)
    is_computed = models.BooleanField(default=False)

    class Meta:
        db_table = "TBL_DTR_SUMMARY"

class DTRCutoff(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    cutoff_code = models.ForeignKey("Cutoff", on_delete=models.CASCADE)
    
    business_date_from = models.DateField()
    business_date_to = models.DateField()

    paid_leaves_total = models.PositiveSmallIntegerField(null=True, blank=True)
    leaves_type_used = models.TextField(max_length=100, null=True, blank=True)
    reg_ot_total = models.PositiveSmallIntegerField(null=True, blank=True)
    nd_ot_total = models.PositiveSmallIntegerField(null=True, blank=True)
    sp_holiday_total = models.PositiveSmallIntegerField(null=True, blank=True)
    sp_holiday_total_hours = models.PositiveSmallIntegerField(null=True, blank=True)
    reg_holiday_total = models.PositiveSmallIntegerField(null=True, blank=True)
    rd_ot_total_hours = models.PositiveSmallIntegerField(null=True, blank=True)
    rd_sp_holiday_ot_total_hours = models.PositiveSmallIntegerField(null=True, blank=True)
    rd_reg_holiday_ot_total_hours = models.PositiveSmallIntegerField(null=True, blank=True)
    
    absent_total = models.PositiveSmallIntegerField(null=True, blank=True)
    overbreak_total = models.PositiveSmallIntegerField(null=True, blank=True)
    lates_total = models.PositiveSmallIntegerField(null=True, blank=True)
    undertime_total = models.PositiveSmallIntegerField(null=True, blank=True)

    total_hours = models.PositiveSmallIntegerField()

    is_processed = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_DTR_CUTOFF_SUMMARY"

class Holiday(models.Model):
    holiday_date = models.DateField()
    holiday_description = models.TextField(max_length=75, null=True, blank=True)
    holiday_type = models.CharField(max_length=5, choices=HOLIDAY_TYPE)
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
    obt_approval_status = models.CharField(max_length=3, choices=APPROVAL_STATUS, default="P1")
    obt_reason_disapproval = models.TextField(max_length=50, null=True, blank=True)
    obt_total_hour = models.PositiveSmallIntegerField()
    obt_approver1_empno = models.PositiveSmallIntegerField(null=True, blank=True)
    obt_date_approved1 = models.DateTimeField(null=True, blank=True)
    obt_approver2_empno = models.PositiveSmallIntegerField(null=True, blank=True)
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
    ot_approval_status = models.CharField(max_length=3, choices=APPROVAL_STATUS, default="P1")
    ot_reason_disapproval = models.TextField(max_length=100, null=True, blank=True)
    ot_total_hours = models.PositiveSmallIntegerField()
    ot_approver1_empno = models.PositiveSmallIntegerField(null=True, blank=True)
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
    leave_approval_status = models.CharField(max_length=3, choices=APPROVAL_STATUS, default="P1")
    leave_reason_disapproval = models.TextField(max_length=100, null=True, blank=True)
    leave_total_hours = models.PositiveSmallIntegerField()
    leave_approver1_empno = models.PositiveSmallIntegerField(null=True, blank=True)
    leave_date_approved1 = models.DateTimeField(null=True, blank=True)
    leave_approver2_empno = models.PositiveSmallIntegerField(null=True, blank=True)
    leave_date_approved2 = models.DateTimeField(null=True, blank=True)
    leave_number_days = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "TBL_LEAVES_APP"

class LeavesCredit(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    leave_type_code = models.ForeignKey("LeavesType", on_delete=models.CASCADE)
    allowed_days = models.PositiveSmallIntegerField(null=True, blank=True)
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
    reg_days_total = models.PositiveSmallIntegerField()
    payroll_group_code = models.ForeignKey(PayrollGroup, on_delete=models.CASCADE)
    division_code = models.ForeignKey(Division, on_delete=models.CASCADE)
    co_is_processed = models.BooleanField()
    credit_date = models.DateTimeField()

    class Meta:
        db_table = "TBL_CUTOFF_PERIOD_LIST"

class ScheduleShift(models.Model):
    name = models.CharField(max_length=35)
    time_in = models.TimeField()
    time_out = models.TimeField()
    grace_period = models.PositiveSmallIntegerField(default=0)
    with_overtime = models.BooleanField()
    is_night_shift = models.BooleanField(default=False)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_SCHEDULE_SHIFT"

class ScheduleDaily(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    business_date = models.DateField()
    schedule_shift_code = models.ForeignKey(ScheduleShift, on_delete=models.CASCADE)
    is_restday = models.BooleanField(default=False)
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
    ua_approval_status = models.CharField(max_length=3, choices=APPROVAL_STATUS, default="P1")
    ua_reason_disapproval = models.TextField(max_length=75, null=True, blank=True)
    ua_total_hour = models.PositiveSmallIntegerField()
    ua_approver1_empno = models.PositiveSmallIntegerField(null=True, blank=True)
    ua_date_approved1 = models.DateTimeField(null=True, blank=True)
    ua_approver2_empno = models.PositiveSmallIntegerField(null=True, blank=True)
    ua_date_approved2 = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_UNACCOUNTED_ATT"

class Payroll(models.Model):
    pr_cutoff_code = models.ForeignKey(Cutoff, on_delete=models.CASCADE)
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    emp_cname = models.CharField(max_length=50)
    cutoff_summary_code = models.ForeignKey(DTRCutoff, on_delete=models.CASCADE)
    run_date = models.DateField(auto_now_add=True)
    accnt_no = models.CharField(max_length=25)
    salary_basic = models.FloatField()
    salary_allowance = models.FloatField()
    salary_other = models.FloatField()
    salary_type = models.CharField(max_length=7)
    
    work_days_total = models.FloatField()
    
    daily_salary_basic = models.FloatField()
    daily_salary_allowance = models.FloatField()
    daily_salary_other = models.FloatField()

    leaves_amount_a = models.FloatField()
    ot_amount_a = models.FloatField()
    nd_amount_a = models.FloatField()
    reg_holiday_amount_a = models.FloatField()
    sp_holiday_amount_a = models.FloatField()
    rd_ot_amount_a = models.FloatField(default=0)
    rd_sp_holiday_amount_a = models.FloatField(default=0)
    rd_reg_holiday_amount_a = models.FloatField(default=0)
    
    lates_amount_d = models.FloatField()
    utime_amount_d = models.FloatField()
    
    sssc_amount_d = models.FloatField()
    sss_cashloan_d = models.FloatField(default=0)
    sss_calloan_d = models.FloatField(default=0)
    
    pagibigc_amount_d = models.FloatField()
    pagibig_cloan_d = models.FloatField(default=0)
    pagibig_hloan_d = models.FloatField(default=0)
    pagibig_calloan_d = models.FloatField(default=0)

    philhealthc_amount_d = models.FloatField()
    
    cash_advance_amount_d = models.FloatField()

    insurance_d = models.FloatField()
    other_d = models.FloatField()

    gross_pay = models.FloatField()
    tax_amount_d = models.FloatField()
    net_pay = models.FloatField()

    absent_amount = models.FloatField()
    date_deleted = models.DateTimeField(null=True, blank=True)
    is_payslip_printed = models.BooleanField(default=False)

    class Meta:
        db_table = "TBL_PAYROLL_RUN"

class CashAdvance(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    cash_advance_total = models.FloatField()
    cash_advance_remaining = models.FloatField()
    payment_monthly = models.FloatField()
    is_fully_paid = models.BooleanField(default=False)
    last_payment_amount = models.FloatField(null=True, blank=True)
    date_last_payment = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "TBL_CASH_ADVANCE"

class AllowanceType(models.Model):
    allowance_name = models.CharField(max_length=50)
    taxable = models.BooleanField(default=False)

    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_ALLOWANCE_TYPE"
    
class AllowanceEntry(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    allowance_code = models.ForeignKey(AllowanceType, on_delete=models.CASCADE)
    amount = models.FloatField()
    tax_rate = models.FloatField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "TBL_ALLOWANCE_ENTRY"

class TaxCollected(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    cutoff_code = models.ForeignKey(Cutoff, on_delete=models.CASCADE)
    allowance_entry_code = models.ForeignKey(AllowanceEntry, on_delete=models.CASCADE)
    tax_rate_used = models.FloatField()
    amount_deducted = models.FloatField()

    date_added = models.DateTimeField(auto_now_add=True)    

    class Meta:
        db_table = "TBL_TAX_COLLECTED"

class SSSBracket(models.Model):
    ramount_from = models.FloatField()
    ramount_to = models.FloatField()
    amount_rate = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_SSS_BRACKET"

class TaxBasicBracket(models.Model):
    frequency = models.PositiveSmallIntegerField()
    ramount_from = models.FloatField()
    ramount_to = models.FloatField()
    amount_rate = models.FloatField()
    fix_tax_amount = models.FloatField(default=0)

    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_TAX_BASIC_BRACKET"

class TaxAllowanceBracket(models.Model):
    ramount_from = models.FloatField()
    ramount_to = models.FloatField()
    amount_rate = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "TBL_TAX_ALLOWA_BRACKET"

class Pay13TH(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    coverage_from = models.DateTimeField()
    coverage_to = models.DateTimeField()
    total_pay = models.FloatField()
    is_printed = models.BooleanField(default=False)

    class Meta:
        db_table = "TBL_13TH_MPAY"

class Announcement(models.Model):
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField()
    is_posted = models.BooleanField()
    expiry_date = models.DateTimeField()
    order_by_no = models.PositiveSmallIntegerField(validators=[MaxValueValidator(3)])
    message = models.TextField(max_length=300)

    class Meta:
        db_table = "TBL_ANNOUNCEMENT_LIST"

class AssetsAccount(models.Model):
    asset_list_code = models.ForeignKey("AssetsLists", on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE, related_name="assignedby")
    assigned_to = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE, related_name="assignedto")
    serial_no_manufacturer = models.CharField(max_length=30)
    serial_no_internal = models.CharField(max_length=30)
    remarks = models.TextField(max_length=100)

    class Meta:
        db_table = "TBL_ASSETS_ACCOUNT_LIST"

class AssetsLists(models.Model):
    asset_name = models.CharField(max_length=25)
    added_by = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=4)
    year = models.DateField()
    batch_no = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(max_length=100)
    remarks = models.TextField(max_length=100, null=True, blank=True)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "TBL_ASSETS_LIST"\
        
class BonusList(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=100)
    amount = models.FloatField()

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "TBL_BONUS_LIST"

class BonusEntry(models.Model):
    bonus_code = models.ForeignKey(BonusList, on_delete=models.CASCADE)
    emp_no = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE)
    cutoff_code = models.ForeignKey(Cutoff, on_delete=models.CASCADE)
    is_applied = models.BooleanField(default=False)
    added_by = models.ForeignKey(Employee, to_field="emp_no", on_delete=models.CASCADE, related_name="added_by_emp_no")

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "TBL_BONUS_ENTRY"