from django.shortcuts import get_object_or_404

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from user.models import *
from user.serializers import *

import secret, jwt
from datetime import datetime, timedelta, date

from user.functionalities.employee_process import upload_csv_file_employee
from user.functionalities.dtr_process import dtr_logs_upload, merge_dtr_entries, create_dtr_cutoff_summary
from user.functionalities.payroll_process import create_payroll



# User Dashboard
class LoginView(APIView):
    @staticmethod
    def post(request):
        username = request.data["username"]
        password = request.data["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found!")
        
        if user.is_locked:
            return Response({"message": "Your account is locked! Make a proper request on your HR regarding this issue. :)"}, status=status.HTTP_403_FORBIDDEN)
        
        if not user.check_password(password):
            if user.failed_login_attempts == 3:
                user.is_locked = True
                user.save()
                return Response({"message": "We lock your account due to security purposes. If you want to login again, contact your HR to inform them about this matter."}, status=status.HTTP_403_FORBIDDEN)
            else:
                user.failed_login_attempts += 1
                user.save()
                raise AuthenticationFailed(f"Incorrect password! You only have {3 - user.failed_login_attempts} attempts left")
            
        user.failed_login_attempts = 0
        user.is_locked = False
        user.last_login = datetime.now()
        user.save()
        user_serializer = UserSerializer(user)

        employee = get_object_or_404(Employee, emp_no=user_serializer.data["emp_no"])
        employee_serializer = EmployeeSerializer(employee)

        payload = {
            "id": user.id,
            "exp": datetime.now() + timedelta(minutes=60),
            "iat": datetime.now()
        }
        token = jwt.encode(payload=payload, key=secret.JWT_SECRET, algorithm="HS256")
        data = {
            "jwt": token,
            "user": user_serializer.data,
            "employee_detail": employee_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    
class UserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response({"ID is required to use this method"}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, pk=pk, date_deleted__isnull=True)
        user.date_deleted = datetime.now()
        user.save()
        return Response({"Message": f"User {pk} account has been successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
# Employee Dashboard
class EmployeesView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, emp_no=None, *args, **kwargs):
        if emp_no is not None:
            employee = get_object_or_404(Employee, emp_no=emp_no, date_deleted__isnull=True)
            serializer = SpecificEmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            employees = Employee.objects.filter(date_deleted__exact=None)
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, emp_no, *args, **kwargs):
        employee = get_object_or_404(Employee, emp_no=emp_no)
        serializer = EmployeeSerializer(employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, emp_no, *args, **kwargs):
        if emp_no is None:
            return Response({"Employee number is required to use this method"}, status=status.HTTP_400_BAD_REQUEST)
        employee = get_object_or_404(Employee, emp_no=emp_no, date_deleted__isnull=True)
        employee.date_deleted = date.today()
        employee.save()
        
        return Response({"message": "Account successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class EmployeeUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        filename = str(file)
        if not file:
            return Response({"Message": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if filename.endswith('.csv'):
                response = upload_csv_file_employee(file)
                return response
            else:                
                return Response({"Message": "The file you uploaded cannot be processed due to incorrect file extension"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)    

class BranchView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            branch = get_object_or_404(Branch, pk=pk, date_deleted__isnull=True)
            branch_serializer = BranchSerializer(branch)
            return Response(branch_serializer.data, status=status.HTTP_200_OK)
        branch = Branch.objects.filter(date_deleted__isnull=True)
        branch_serializer = BranchSerializer(branch, many=True)
        return Response(branch_serializer.data, status=status.HTTP_200_OK)\
        
    def post(self, request, *args, **kwargs):
        branch_serializer = BranchSerializer(data=request.data)
        if branch_serializer.is_valid():
            branch_serializer.save()
            return Response(branch_serializer.data, status=status.HTTP_201_CREATED)
        return Response(branch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None, *args, **kwargs):
        branch = get_object_or_404(Branch,pk=pk, date_deleted__isnull=True)
        branch_serializer = BranchSerializer(branch, data=request.data)
        if branch_serializer.is_valid():
            branch_serializer.save()
            return Response(branch_serializer.data, status=status.HTTP_200_OK)
        return Response(branch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response({"Message": "It requires ID to delete a branch instance"}, status=status.HTTP_400_BAD_REQUEST)
        branch = get_object_or_404(Branch, pk=pk, date_deleted__isnull=True)
        branch.date_deleted = datetime.now()
        branch.save()
        return Response({"Message": f"Branch {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class DepartmentView(APIView):
    def get (self, request, pk=None, *args, **kwargs):
        if pk is not None:
            department = get_object_or_404(Department, pk=pk, date_deleted__isnull=True)
            department_serializer = DepartmentSerializer(department)
            return Response(department_serializer.data, status=status.HTTP_200_OK)
        department = Department.objects.filter(date_deleted__isnull=True)
        department_serializer = DepartmentSerializer(department, many=True)
        return Response(department_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        department_serializer = DepartmentSerializer(data=request.data)
        if department_serializer.is_valid(raise_exception=True):
            department_serializer.save()
            return Response(department_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk, date_deleted__isnull=True)
        department_serializer = DepartmentSerializer(department, data=request.data)
        if department_serializer.is_valid(raise_exception=True):
            department_serializer.save()
            return Response(department_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk, date_deleted__isnull=True)
        department.date_deleted = datetime.now()
        department.save()
        return Response({"Message": f"Department {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

class DivisionView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            division = get_object_or_404(Division, pk=pk, date_deleted__isnull=True)
            division_serializer = DivisionSerializer(division)
            return Response(division_serializer.data, status=status.HTTP_200_OK)
        division = Division.objects.filter(date_deleted__isnull=True)
        division_serializer = DivisionSerializer(division, many=True)
        return Response(division_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        division_serializer = DivisionSerializer(data=request.data)
        if division_serializer.is_valid(raise_exception=True):
            division_serializer.save()
            return Response(division_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None, *args, **kwargs):
        division = get_object_or_404(Division, pk=pk, date_deleted__isnull=True)
        division_serializer = DivisionSerializer(division, data=request.data)
        if division_serializer.is_valid(raise_exception=True):
            division_serializer.save()
            return Response(division_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, *args, **kwargs):
        division = get_object_or_404(Division, pk=pk, date_deleted__isnull=True)
        division.date_deleted = datetime.now()
        division.save()
        return Response({"Message": f"Division {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class PayrollGroupView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            payrollgroup = get_object_or_404(PayrollGroup, pk=pk, date_deleted__isnull=True)
            payrollgroup_serializer = PayrollGroupSerializer(payrollgroup)
            return Response(payrollgroup_serializer.data, status=status.HTTP_200_OK)
        payrollgroup = PayrollGroup.objects.filter(date_deleted__isnull=True)
        payrollgroup_serializer = PayrollGroupSerializer(payrollgroup, many=True)
        return Response(payrollgroup_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        payrollgroup_serializer = PayrollGroupSerializer(data=request.data)
        if payrollgroup_serializer.is_valid(raise_exception=True):
            payrollgroup_serializer.save()
            return Response(payrollgroup_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None, *args, **kwargs):
        payrollgroup = get_object_or_404(PayrollGroup, pk=pk)
        payrollgroup_serializer = PayrollGroupSerializer(payrollgroup, data=request.data)
        if payrollgroup_serializer.is_valid(raise_exception=True):
            payrollgroup_serializer.save()
            return Response(payrollgroup_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, *args, **kwargs):
        payrollgroup = get_object_or_404(PayrollGroup, pk=pk, date_deleted__isnull=True)
        payrollgroup.date_deleted = datetime.now()
        payrollgroup.save()
        return Response({"Message": f"Payroll Group ID {pk} has been successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class PositionView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            position = get_object_or_404(Position, pk=pk, date_deleted__isnull=True)
            position_serializer = PositionSerializer(position)
            return Response(position_serializer.data, status=status.HTTP_200_OK)
        position = Position.objects.filter(date_deleted__isnull=True)
        position_serializer = PositionSerializer(position, many=True)
        return Response(position_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        position_serializer = PositionSerializer(data=request.data)
        if position_serializer.is_valid(raise_exception=True):
            position_serializer.save()
            return Response(position_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None, *args, **kwargs):
        position = get_object_or_404(Position, pk=pk)
        position_serializer = PositionSerializer(position, data=request.data)
        if position_serializer.is_valid(raise_exception=True):
            position_serializer.save()
            return Response(position_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, *args, **kwargs):
        position = get_object_or_404(Position, pk=pk, date_deleted__isnull=True)
        position.date_deleted = datetime.now()
        position.save()
        return Response({"Message": f"Position ID {pk} has been successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

class BirthdayView(APIView):
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        employees = sorted(employees, key=lambda e: e.days_before(e.birthday))
        employees = employees[:50]
        data = []

        for employee in employees:
            days_before_birthday = employee.days_before(employee.birthday)
            employee_data = {
                "name": f"{employee.first_name} {employee.last_name}",
                "birthday": employee.birthday.strftime("%Y-%m-%d"),
                "days_before_birthday": days_before_birthday
            }
            data.append(employee_data)

        return Response(data, status=status.HTTP_200_OK)
    
class AnniversaryView(APIView):
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        employees = sorted(employees, key=lambda e: e.days_before(e.date_hired))
        employees = employees[:50]
        data = []

        for employee in employees:
            days_before_anniv = employee.days_before(employee.date_hired)
            employee_data = {
                "name": f"{employee.first_name} {employee.last_name}",
                "anniversary": employee.date_hired.strftime("%Y-%m-%d"),
                "days_before_anniv": days_before_anniv
            }
            data.append(employee_data)

        return Response(data, status=status.HTTP_200_OK)        
        
        
            
# DTR Dashboard
class DTRView(APIView):
    def get(self, request, emp_no=None, *args, **kwargs):
        if emp_no is not None:
            dtr = DTR.objects.filter(emp_no=emp_no)
            serializer = DTRSerializer(dtr, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            dtr = DTR.objects.all()
            serializer = DTRSerializer(dtr, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class UploadDTREntryView(APIView):
    def post(self, request, *args, **kwargs):
        tsv_file = request.FILES.get('file')
        tsv_filename = str(tsv_file)

        if not tsv_file:
            return Response({"message": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)    
        else:
            if tsv_filename.endswith(".tsv"):
                response = dtr_logs_upload(tsv_file)
                return response
            else:
                return Response({"Message": "The file you uploaded cannot be processed due to incorrect file extension"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)                

class DTRSummaryView(APIView):
    def get(self, request, emp_no=None, cutoff_code=None, *args, **kwargs):
        cutoff_code = request.data['cutoff_code']

        if emp_no is not None and cutoff_code is None:
            dtr_summary = DTRSummary.objects.filter(emp_no=emp_no)
            dtr_summary_serializer = DTRSummarySerializer(dtr_summary, many=True)
            return Response(dtr_summary_serializer.data, status=status.HTTP_200_OK)
        elif emp_no is not None and cutoff_code is not None:
            dtr_summary = DTRSummary.objects.filter(emp_no=emp_no, cutoff_code=cutoff_code)
            dtr_summary_serializer = DTRSummarySerializer(dtr_summary, many=True)
            return Response(dtr_summary_serializer.data, status=status.HTTP_200_OK)

        dtr_summary = DTRSummary.objects.all()
        dtr_summary_serializer = DTRSummarySerializer(dtr_summary, many=True)
        return Response(dtr_summary_serializer.data, status=status.HTTP_200_OK)


class CutoffPeriodListView(APIView):
    def get(self, request, pk=None, *args, **kwargs):                
        if pk is not None:
            cutoff = Cutoff.objects.get(pk=pk)            
            payroll_group_code = cutoff.payroll_group_code
            employees = Employee.objects.filter(payroll_group_code=payroll_group_code)
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            cutoff = Cutoff.objects.all()
            serializer = CutoffSerializer(cutoff, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class MergeDTRSummaryView(APIView):
    def post(self, request, *args, **kwargs):
        user_emp_nos = request.data["emp_no"]
        cutoff_code = request.data["cutoff_code"]
        cutoff = get_object_or_404(Cutoff, pk=cutoff_code)
        payroll_group_code = cutoff.payroll_group_code

        if user_emp_nos:
            employees = Employee.objects.filter(emp_no__in=user_emp_nos, payroll_group_code=payroll_group_code, date_deleted=None)            
            response = merge_dtr_entries(employees, cutoff_code, operation="list")

            return response

        else:
            employees = Employee.objects.filter(payroll_group_code=payroll_group_code, date_deleted=None)        
            response = merge_dtr_entries(employees, cutoff_code, operation="null")

            return response        
    
class DTRCutoffSummaryView(APIView):
    def get(self, request, emp_no=None, *args, **kwargs):
        cutoff_code = request.data['cutoff_code']
        if emp_no is not None and cutoff_code is None:
            dtr_cutoff = DTRCutoff.objects.filter(emp_no=emp_no, date_deleted__isnull=True)
            dtr_cutoff_serializer = DTRCutoffSerializer(dtr_cutoff, many=True)
            return Response(dtr_cutoff_serializer.data, status=status.HTTP_200_OK)
        elif emp_no is not None and cutoff_code is not None:
            dtr_cutoff = DTRCutoff.objects.filter(emp_no=emp_no, cutoff_code=cutoff_code, date_deleted__isnull=True)
            dtr_cutoff_serializer = DTRCutoffSerializer(dtr_cutoff, many=True)
            return Response(dtr_cutoff_serializer.data, status=status.HTTP_200_OK)
        dtr_cutoff = DTRCutoff.objects.filter(date_deleted__isnull=True)
        dtr_cutoff_serializer = DTRCutoffSerializer(dtr_cutoff, many=True)
        return Response(dtr_cutoff_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response({"ID is required to use this method"}, status=status.HTTP_400_BAD_REQUEST)
        
        dtr_cutoff = get_object_or_404(DTRCutoff, pk=pk)
        dtr_cutoff.date_deleted = datetime.now()
        dtr_cutoff.save()
        return Response({"Message": f"DTR Cutoff Summary {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class CreateDTRCutoffSummaryView(APIView):
    def post(self, request, *args, **kwargs):
        user_emp_nos = request.data['emp_no']
        cutoff_code = request.data['cutoff_code']
        cutoff = Cutoff.objects.get(pk=cutoff_code)
        payroll_group_code = cutoff.payroll_group_code
        cutoff_start_date = cutoff.co_date_from
        cutoff_end_date = cutoff.co_date_to

        if user_emp_nos:
            employees = Employee.objects.filter(emp_no__in=user_emp_nos, payroll_group_code=payroll_group_code)
            operation = "list"
            response = create_dtr_cutoff_summary(employees, cutoff_code, cutoff_start_date, cutoff_end_date, operation)

            return response

        else:
            employees = Employee.objects.filter(payroll_group_code=payroll_group_code, date_deleted=None)
            print(employees)
            operation = "null"
            response = create_dtr_cutoff_summary(employees, cutoff_code, cutoff_start_date, cutoff_end_date, operation)

            return response            
    
# Payroll Dashboard
class PayrollView(APIView):
    def get(self, request, emp_no=None, *args, **kwargs):
        if emp_no is not None:
            payrolls = Payroll.objects.filter(emp_no=emp_no)
            payrolls_serializer = PayrollViewSerializer(payrolls, many=True)
            return Response(payrolls_serializer.data, status=status.HTTP_200_OK)
        payrolls = Payroll.objects.all()
        serializer = PayrollViewSerializer(payrolls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreatePayrollView(APIView):
    def post(self, request, *args, **kwargs):
        is_loan = request.data['is_loan']
        is_ca = request.data['is_ca']
        is_pagibig_house = request.data['is_pagibig_house']
        is_pagibig_cal = request.data['is_pagibig_cal']
        is_pagibig_cash = request.data['is_pagibig_cash']
        is_sss_cal = request.data['is_sss_cal']
        is_sss_cash = request.data['is_sss_cash']
        is_deduction = request.data['is_deduction']
        is_30 = request.data['is_30']
        is_70 = request.data['is_70']

        user_emp_nos = request.data['emp_no']
        cutoff_code = request.data['cutoff_code']
        cutoff = Cutoff.objects.get(pk=cutoff_code)

        if user_emp_nos:
            employees = Employee.objects.filter(emp_no__in=user_emp_nos, payroll_group_code=cutoff.payroll_group_code, date_deleted=None)
            response = create_payroll(employees, cutoff, is_loan, is_ca, is_pagibig_house, is_pagibig_cal, is_pagibig_cash, is_sss_cal, is_sss_cash, is_deduction, is_30, is_70, operation="list")

            return response
        
        else:
            employees = Employee.objects.filter(payroll_group_code=cutoff.payroll_group_code, date_deleted=None)
            response = create_payroll(employees, cutoff, is_loan, is_ca, is_pagibig_house, is_pagibig_cal, is_pagibig_cash, is_sss_cal, is_sss_cash, is_deduction, is_30, is_70, operation="null")

            return response

