from rest_framework import serializers
from user.models import *



class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = "__all__"

class PayrollGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollGroup
        fields = "__all__"

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = "__all__"

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = "__all__"

class CityMunicipalitySerializer(serializers.ModelSerializer):
    # Include the code below to access the fields you want to add in your API
    # province_name = serializers.CharField(source="province.name", read_only=True)
    data = serializers.SerializerMethodField()
    
    class Meta:
        model = CityMunicipality
        fields = ["id", "name", "data"]

    def get_data(self, obj):
        return {'province': obj.province.id, "province_name":obj.province.name}

class ProvinceSerializer(serializers.ModelSerializer):
    # Include code below if you want to enable the parent model to access the data on the child model
    citymunicipality_set = CityMunicipalitySerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = ("id", "name", "citymunicipality_set")

class PAGIBIGSerializer(serializers.ModelSerializer):
    class Meta:
        model = PAGIBIG
        fields = "__all__"

class SSSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSS
        fields = "__all__"

class PhilhealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Philhealth
        fields = "__all__"

class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = "__all__"

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = "__all__"

class OBTSerializer(serializers.ModelSerializer):
    class Meta:
        model = OBT
        fields = "__all__"

class OvertimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = "__all__"

class LeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = "__all__"
        
class LeavesCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavesCredit
        fields = "__all__"

class GetLeavesCreditSerializer(serializers.ModelSerializer):
    leave_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LeavesCredit
        fields = "__all__"

    def get_leave_name(self, obj):
        try:
            leave_name = LeavesType.objects.get(pk=obj.leave_type_code.pk)
            return LeavesTypeSerializer(leave_name).data['name']
        except LeavesType.DoesNotExist:
            return None

class LeavesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavesType
        fields = "__all__"

class AdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjustment
        fields = "__all__"

class CutoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cutoff
        fields = "__all__"

class ScheduleShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleShift
        fields = "__all__"

class GetScheduleDailySerializer(serializers.ModelSerializer):
    schedule_shift_code = ScheduleShiftSerializer()
    class Meta:
        model = ScheduleDaily
        fields = "__all__"

class ScheduleDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleDaily
        fields = "__all__"

class ScheduleDailyDFSerializer(serializers.ModelSerializer):
    time_in = serializers.SerializerMethodField()
    time_out = serializers.SerializerMethodField()
    bio_id = serializers.SerializerMethodField()
    class Meta:
        model = ScheduleDaily
        fields = ['id', 'time_in', 'time_out', 'business_date', 'emp_no', 'bio_id']

    def get_time_in(self, obj):
        try:
            schedule_shift_timein = ScheduleShift.objects.get(pk=obj.schedule_shift_code.pk)
            return ScheduleShiftSerializer(schedule_shift_timein).data['time_in']
        except ScheduleShift.DoesNotExist:
            return None
        
    def get_time_out(self, obj):
        try:
            schedule_shift_timeout = ScheduleShift.objects.get(pk=obj.schedule_shift_code.pk)
            return ScheduleShiftSerializer(schedule_shift_timeout).data['time_out']
        except ScheduleShift.DoesNotExist:
            return None
    
    def get_bio_id(self, obj):
        try:
            employee = Employee.objects.get(emp_no=obj.emp_no.emp_no)
            return EmployeeSerializer(employee).data['bio_id']
        except Employee.DoesNotExist:
            return None

class DTRCutoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = DTRCutoff
        fields = "__all__"

class UnaccountedAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnaccountedAttendance
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        # prevent password from returning on json file
        extra_kwargs = {
            "password": {"write_only":True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
    
class SpecificEmployeeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    employee_image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True, required=False)
    class Meta:
        model = Employee
        fields = "__all__"

    def get_user(self, obj):
        try:
            user = User.objects.get(emp_no=obj.emp_no)
            return UserSerializer(user).data
        except User.DoesNotExist:
            return None
        
class EmployeeSerializer(serializers.ModelSerializer):
    employee_image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True, required=False)
    class Meta:
        model = Employee
        fields = "__all__"
        
class DTRSerializer(serializers.ModelSerializer):

    # Di ko alam bakit may ganito
    # emp_no = EmployeeSerializer()
    # bio_id = EmployeeSerializer()
    # branch_code = BranchSerializer()
    # schedule_daily_code = ScheduleDailySerializer()

    class Meta:
        model = DTR
        fields = "__all__"

class DTRSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DTRSummary
        fields = "__all__"

class DTRCutoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = DTRCutoff
        fields = "__all__"

class PayrollViewSerializer(serializers.ModelSerializer):
    cutoff = serializers.SerializerMethodField()
    dtr_cutoff = serializers.SerializerMethodField()
    class Meta:
        model = Payroll
        fields = "__all__"

    def get_cutoff(self, obj):
        try:
            cutoff= Cutoff.objects.get(pk=obj.pr_cutoff_code.pk)
            return CutoffSerializer(cutoff).data
        except Cutoff.DoesNotExist:
            return None
        
    def get_dtr_cutoff(self, obj):
        try:
            dtr_cutoff = DTRCutoff.objects.get(pk=obj.cutoff_summary_code.pk)
            return DTRCutoffSerializer(dtr_cutoff).data
        except DTRCutoff.DoesNotExist:
            return None

class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = "__all__"

class CashAdvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashAdvance
        fields = "__all__"

class AllowanceEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowanceEntry
        fields = "__all__"

class AllowanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowanceType
        fields = "__all__"

class TaxCollectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxCollected
        fields = "__all__"

class SSSBracketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSSBracket
        fields = "__all__"

class TaxBasicBracketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxBasicBracket
        fields = "__all__"

class TaxAllowanceBracketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxAllowanceBracket
        fields = "__all__"

class Pay13THSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay13TH
        fields = "__all__"

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"

class AssestsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetsLists
        fields = "__all__"

class AssetsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetsAccount
        fields = "__all__"

class BonusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusList
        fields = "__all__"

class BonusEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusEntry
        fields = "__all__"