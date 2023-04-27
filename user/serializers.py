from rest_framework import serializers
from user.models import User, Employee, AuditTrail

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'employee_id', 'username', 'password', 'date_added', 'is_active', 
              'date_deleted', 'is_locked', 'failed_login_attempts', 'old_password', 
              'date_password_change', 'role', 'last_login', ]

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'first_name', 'middle_name', 
                  'last_name', 'suffix', 'birthday', 'gender', 'address', 
                  'provincial_address', 'mobile_phone', 'email', 'approver', 
                  'date_hired', 'date_resigned', 'department_code', 'division_code', 
                  'position_code', 'rank_code', 'city_code', 'payroll_group_code', 
                  'tax_code', 'sssid_code', 'philhealth_code', 'date_added', 'date_deleted']

class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = ['id', 'employee_id', 'transaction_type', 'table_affected', 'action_remarks', 'date_added']