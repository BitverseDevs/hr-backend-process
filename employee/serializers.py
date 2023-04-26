from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'first_name', 'middle_name', 
                  'last_name', 'suffix', 'birthday', 'gender', 'address', 
                  'provincial_address', 'mobile_phone', 'email', 'approver', 
                  'date_hired', 'date_resigned', 'department_code', 'division_code', 
                  'position_code', 'rank_code', 'city_code', 'payroll_group_code', 
                  'tax_code', 'sssid_code', 'philhealth_code', 'date_added', 'date_deleted']