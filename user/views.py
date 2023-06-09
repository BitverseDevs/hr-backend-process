from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from user.models import *
from user.serializers import *

import secret, jwt
from datetime import datetime, timedelta, date, time

from user.functionalities.employee_process import upload_csv_file_employee
from user.functionalities.dtr_process import dtr_logs_upload, merge_dtr_entries, create_dtr_cutoff_summary, new_dtr_logs_upload, new_merge_dtr_entries, newest_dtr_logs_upload
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
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED) 
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(User, pk=pk, date_deleted__isnull=True)
        user.date_deleted = datetime.now()
        user.save()
        return Response({"Message": f"User Account ID {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    


# Employee Dashboard
class EmployeesView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, emp_no=None, *args, **kwargs):
        if emp_no is not None:
            employee = get_object_or_404(Employee, emp_no=emp_no, date_deleted__isnull=True)
            employee_serializer = SpecificEmployeeSerializer(employee)
            return Response(employee_serializer.data, status=status.HTTP_200_OK)
        employees = Employee.objects.filter(date_deleted__exact=None)
        employees_serializer = EmployeeSerializer(employees, many=True)
        return Response(employees_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        employee_serializer = EmployeeSerializer(data=request.data)
        if employee_serializer.is_valid(raise_exception=True):
            employee_serializer.save()
            return Response(employee_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, emp_no=None, *args, **kwargs):
        employee = get_object_or_404(Employee, emp_no=emp_no)
        employee_serializer = EmployeeSerializer(employee, data=request.data)
        if employee_serializer.is_valid(raise_exception=True):
            employee_serializer.save()
            return Response(employee_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, emp_no=None, *args, **kwargs):
        employee = get_object_or_404(Employee, emp_no=emp_no, date_deleted__isnull=True)
        employee.date_deleted = date.today()
        employee.save()
        return Response({"message": f"Employee ID {emp_no} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
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
        if branch_serializer.is_valid(raise_exception=True):
            branch_serializer.save()
            return Response(branch_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(branch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None, *args, **kwargs):
        branch = get_object_or_404(Branch,pk=pk, date_deleted__isnull=True)
        branch_serializer = BranchSerializer(branch, data=request.data)
        if branch_serializer.is_valid(raise_exception=True):
            branch_serializer.save()
            return Response(branch_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(branch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, *args, **kwargs):
        branch = get_object_or_404(Branch, pk=pk, date_deleted__isnull=True)
        branch.date_deleted = datetime.now()
        branch.save()
        return Response({"Message": f"Branch ID {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
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
        else:
            return Response(department_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk, date_deleted__isnull=True)
        department_serializer = DepartmentSerializer(department, data=request.data)
        if department_serializer.is_valid(raise_exception=True):
            department_serializer.save()
            return Response(department_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(department_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk, date_deleted__isnull=True)
        department.date_deleted = datetime.now()
        department.save()
        return Response({"Message": f"Department ID {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

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
        else:
            return Response(division_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        division = get_object_or_404(Division, pk=pk, date_deleted__isnull=True)
        division_serializer = DivisionSerializer(division, data=request.data)
        if division_serializer.is_valid(raise_exception=True):
            division_serializer.save()
            return Response(division_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(division_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        division = get_object_or_404(Division, pk=pk, date_deleted__isnull=True)
        division.date_deleted = datetime.now()
        division.save()
        return Response({"Message": f"Division ID {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
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
        else:
            return Response(payrollgroup_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        payrollgroup = get_object_or_404(PayrollGroup, pk=pk)
        payrollgroup_serializer = PayrollGroupSerializer(payrollgroup, data=request.data)
        if payrollgroup_serializer.is_valid(raise_exception=True):
            payrollgroup_serializer.save()
            return Response(payrollgroup_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(payrollgroup_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        else:
            return Response(position_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        position = get_object_or_404(Position, pk=pk)
        position_serializer = PositionSerializer(position, data=request.data)
        if position_serializer.is_valid(raise_exception=True):
            position_serializer.save()
            return Response(position_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(position_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        position = get_object_or_404(Position, pk=pk, date_deleted__isnull=True)
        position.date_deleted = datetime.now()
        position.save()
        return Response({"Message": f"Position ID {pk} has been successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class RankView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            rank = get_object_or_404(Rank, pk=pk, date_deleted__isnull=True)
            rank_serializer = RankSerializer(rank)
            return Response(rank_serializer.data, status=status.HTTP_200_OK)
        rank = Rank.objects.filter(date_deleted__isnull=True)
        rank_serializer = RankSerializer(rank, many=True)
        return Response(rank_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        rank_serializer = RankSerializer(data=request.data)
        if rank_serializer.is_valid(raise_exception=True):
            rank_serializer.save()
            return Response(rank_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(rank_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        rank = get_object_or_404(Rank, pk=pk)
        rank_serializer = RankSerializer(rank, data=request.data)
        if rank_serializer.is_valid(raise_exception=True):
            rank_serializer.save()
            return Response(rank_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(rank_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        rank = get_object_or_404(Rank, pk=pk, date_deleted__isnull=True)
        rank.date_deleted = datetime.now()
        rank.save()
        return Response({"Message": f"Rank ID {pk} has been successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

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



# Employment Details
class HolidayView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            holiday = get_object_or_404(Holiday, pk=pk)
            holiday_serializer = HolidaySerializer(holiday)
            return Response(holiday_serializer.data, status=status.HTTP_200_OK)
        holiday = Holiday.objects.all().order_by('holiday_date')
        holiday_serializer = HolidaySerializer(holiday, many=True)
        return Response(holiday_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        holiday_serializer = HolidaySerializer(data=request.data)
        if holiday_serializer.is_valid(raise_exception=True):
            holiday_serializer.save()
            return Response(holiday_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(holiday_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        holiday = get_object_or_404(Holiday, pk=pk)
        holiday_serializer = HolidaySerializer(holiday, data=request.data)
        if holiday_serializer.is_valid(raise_exception=True):
            holiday_serializer.save()
            return Response(holiday_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(holiday_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OBTView(APIView):
    def get(self, request, emp_no=None, pk=None, *args, **kwargs):
        if emp_no is not None and pk is None:
            obt = OBT.objects.filter(emp_no=emp_no)
            obt_serializer = OBTSerializer(obt, many=True)
            return Response(obt_serializer.data, status=status.HTTP_200_OK)
        elif emp_no is not None and pk is not None:
            obt = get_object_or_404(OBT, emp_no=emp_no, pk=pk)
            obt_serializer = OBTSerializer(obt)
            return Response(obt_serializer.data, status=status.HTTP_200_OK)
        obt = OBT.objects.all()
        obt_serializer = OBTSerializer(obt, many=True)
        return Response(obt_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        obt_serializer = OBTSerializer(data=request.data)
        if obt_serializer.is_valid(raise_exception=True):
            obt_serializer.save()
            return Response(obt_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(obt_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request,emp_no=None, pk=None, *args, **kwargs):
        obt = get_object_or_404(OBT, emp_no=emp_no, pk=pk)
        obt_serializer = OBTSerializer(obt, data=request.data)
        if obt_serializer.is_valid(raise_exception=True):
            obt_serializer.save()
            return Response(obt_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(obt_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class OBTApproverView(APIView):
    def get(self, request, approver=None, *args, **kwargs):
        obt = OBT.objects.filter(Q(obt_approver1_empno=approver) | Q(obt_approver2_empno=approver))
        obt_serializer = OBTSerializer(obt, many=True)
        return Response(obt_serializer.data, status=status.HTTP_200_OK)
        
class OvertimeView(APIView):
    def get(self, request, emp_no=None, pk=None, *args, **kwargs):
        if emp_no is not None and pk is None:
            ot = Overtime.objects.filter(emp_no=emp_no)
            ot_serializer = OvertimeSerializer(ot, many=True)
            return Response(ot_serializer.data, status=status.HTTP_200_OK)
        elif emp_no is not None and pk is not None:
            ot = get_object_or_404(Overtime, emp_no=emp_no, pk=pk)
            ot_serializer = OvertimeSerializer(ot)
            return Response(ot_serializer.data, status=status.HTTP_200_OK)
        ot = Overtime.objects.all()
        ot_serializer = OvertimeSerializer(ot, many=True)
        return Response(ot_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        ot_serializer = OvertimeSerializer(data=request.data)
        if ot_serializer.is_valid(raise_exception=True):
            ot_serializer.save()
            return Response(ot_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, emp_no=None, pk=None, *args, **kwargs):
        ot = get_object_or_404(Overtime, emp_no=emp_no, pk=pk)
        ot_serializer = OvertimeSerializer(ot, data=request.data)
        if ot_serializer.is_valid(raise_exception=True):
            ot_serializer.save()
            return Response(ot_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(ot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class OTApproverView(APIView):
    def get(self, request, approver=None, *args, **kwargs):
        ot = Overtime.objects.filter(Q(ot_approver1_empno=approver) | Q(ot_approver2_empno=approver))
        ot_serializer = OvertimeSerializer(ot, many=True)
        return Response(ot_serializer.data, status=status.HTTP_200_OK)
        
class LeaveTypeView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            leave_type = get_object_or_404(LeavesType, pk=pk)
            leave_type_serializer = LeavesTypeSerializer(leave_type)
            return Response(leave_type_serializer.data, status=status.HTTP_200_OK)
        leave_type = LeavesType.objects.all()
        leave_type_serializer = LeavesTypeSerializer(leave_type, many=True)
        return Response(leave_type_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        leave_type_serializer = LeavesTypeSerializer(data=request.data)
        if leave_type_serializer.is_valid(raise_exception=True):
            leave_type_serializer.save()
            return Response(leave_type_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(leave_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None, *args, **kwargs):
        leave_type = get_object_or_404(LeavesType, pk=pk)
        leave_type_serializer = LeavesTypeSerializer(leave_type, data=request.data)
        if leave_type_serializer.is_valid(raise_exception=True):
            leave_type_serializer.save()
            return Response(leave_type_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(leave_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeaveCreditView(APIView):
    def get(self, request, emp_no=None, *args, **kwargs):
        if emp_no is not None:
            leave_credit = get_object_or_404(LeavesCredit, emp_no=emp_no)
            leave_credit_serializer = GetLeavesCreditSerializer(leave_credit)
            return Response(leave_credit_serializer.data, status=status.HTTP_200_OK)
        leave_credit = LeavesCredit.objects.all()
        leave_credit_serializer = GetLeavesCreditSerializer(leave_credit, many=True)
        return Response(leave_credit_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        leave_credit_serializer = LeavesCreditSerializer(data=request.data)
        if leave_credit_serializer.is_valid(raise_exception=True):
            leave_credit_serializer.save()
            return Response(leave_credit_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(leave_credit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None, *args, **kwargs):
        leave_credit = get_object_or_404(LeavesCredit, pk=pk)
        leave_credit_serializer = LeavesCreditSerializer(leave_credit, data=request.data)
        if leave_credit_serializer.is_valid(raise_exception=True):
            leave_credit_serializer.save()
            return Response(leave_credit_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(leave_credit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeaveView(APIView): # Pending Computation
    def get(self, request, emp_no=None, pk=None, *args, **kwargs):
        if emp_no is not None and pk is None:
            leave = Leaves.objects.filter(emp_no=emp_no)
            leave_serializer = LeavesSerializer(leave, many=True)
            return Response(leave_serializer.data, status=status.HTTP_200_OK)
        elif emp_no is not None and pk is not None:
            leave = get_object_or_404(Leaves, emp_no=emp_no, pk=pk)
            leave_serializer = LeavesSerializer(leave)
            return Response(leave_serializer.data, status=status.HTTP_200_OK)
        leave = Leaves.objects.all()
        leave_serializer = LeavesSerializer(leave, many=True)
        return Response(leave_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        leave_serializer = LeavesSerializer(data=request.data)
        if leave_serializer.is_valid(raise_exception=True):
            leave_serializer.save()
            return Response(leave_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(leave_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put (self, request, emp_no=None, pk=None, *args, **kwargs):
        leave = get_object_or_404(Leaves, emp_no=emp_no, pk=pk)
        leave_serializer = LeavesSerializer(leave, data=request.data)
        if leave_serializer.is_valid(raise_exception=True):
            leave_serializer.save()
            return Response(leave_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(leave_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LeaveApproverView(APIView):
    def get(self, request, approver=None, *args, **kwargs):
        leave = Leaves.objects.filter(Q(leave_approver1_empno=approver) | Q(leave_approver2_empno=approver))
        leave_serializer = LeavesSerializer(leave, many=True)
        return Response(leave_serializer.data, status=status.HTTP_200_OK)
        
class UnaccountedAttendanceView(APIView):
    def get(self, request, emp_no=None, pk=None, *args, **kwargs):    
        if emp_no is not None and pk is None:
            ua = UnaccountedAttendance.objects.filter(emp_no=emp_no)
            ua_serializer = UnaccountedAttendanceSerializer(ua, many=True)
            return Response(ua_serializer.data, status=status.HTTP_200_OK)
        elif emp_no is not None and pk is not None:
            ua = get_object_or_404(UnaccountedAttendance, emp_no=emp_no, pk=pk)
            ua_serializer = UnaccountedAttendanceSerializer(ua)
            return Response(ua_serializer.data, status=status.HTTP_200_OK)
        ua = UnaccountedAttendance.objects.all()
        ua_serializer = UnaccountedAttendanceSerializer(ua, many=True)
        return Response(ua_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        ua_serializer = UnaccountedAttendanceSerializer(data=request.data)
        if ua_serializer.is_valid(raise_exception=True):
            ua_serializer.save()
            return Response(ua_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ua_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, emp_no=None, pk=None, *args, **kwargs):
        ua = get_object_or_404(UnaccountedAttendance, emp_no=emp_no, pk=pk)
        ua_serializer = UnaccountedAttendanceSerializer(ua, data=request.data)
        if ua_serializer.is_valid(raise_exception=True):
            ua_serializer.save()
            return Response(ua_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(ua_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UnaccountedAttendanceApproverView(APIView):
    def get(self, request, approver=None, *args, **kwargs):
        ua = UnaccountedAttendance.objects.filter(Q(ua_approver1_empno=approver) | Q(ua_approver2_empno=approver))
        ua_serializer = UnaccountedAttendanceSerializer(ua, many=True)
        return Response(ua_serializer.data, status=status.HTTP_200_OK)
        
class ScheduleShiftView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            shift = get_object_or_404(ScheduleShift, pk=pk, date_deleted__isnull=True)
            shift_serializer = ScheduleShiftSerializer(shift)
            return Response(shift_serializer.data, status=status.HTTP_200_OK)
        shift = ScheduleShift.objects.filter(date_deleted__isnull=True)
        shift_serializer = ScheduleShiftSerializer(shift, many=True)
        return Response(shift_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        time_in = request.data['time_in']
        time_out = request.data['time_out']
        shift_timein = datetime.strptime(time_in, '%H:%M:%S').time()
        shift_timeout = datetime.strptime(time_out, '%H:%M:%S').time()
        night_differential_in = time(22,0,0,0)
        night_differential_out = time(6,0,0,0)
        if shift_timein >= night_differential_in or shift_timein < night_differential_out or shift_timeout > night_differential_in or shift_timeout <=night_differential_out:
            request.data['is_night_shift'] = True
        shift_serializer = ScheduleShiftSerializer(data=request.data)
        if shift_serializer.is_valid(raise_exception=True):
            shift_serializer.save()
            return Response(shift_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(shift_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None, *args, **kwargs):
        shift = get_object_or_404(ScheduleShift, pk=pk)
        shift_serializer = ScheduleShiftSerializer(shift, data=request.data)
        if shift_serializer.is_valid(raise_exception=True):
            shift_serializer.save()
            return Response(shift_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(shift_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk=None, *args, **kwargs):
        shift = get_object_or_404(ScheduleShift, pk=pk)
        shift.date_deleted = datetime.now()
        shift.save()
        return Response({"Message": f"Schedule Shift ID {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

class ScheduleDailyView(APIView):
    def get(self, request, emp_no=None, pk=None, *args, **kwargs):
        if emp_no is not None and pk is None:
            daily = ScheduleDaily.objects.filter(emp_no=emp_no)
            daily_serializer = GetScheduleDailySerializer(daily, many=True)
            return Response(daily_serializer.data, status=status.HTTP_200_OK)
        elif emp_no is not None and pk is not None:
            daily = get_object_or_404(ScheduleDaily, emp_no=emp_no, pk=pk)
            daily_serializer = ScheduleDailySerializer(daily)
            return Response(daily_serializer.data, status=status.HTTP_200_OK)
        daily = ScheduleDaily.objects.all()
        daily_serializer = GetScheduleDailySerializer(daily, many=True)
        return Response(daily_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        daily_serializer = ScheduleDailySerializer(data=request.data)
        if daily_serializer.is_valid(raise_exception=True):
            daily_serializer.save()
            return Response(daily_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(daily_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, emp_no=None, pk=None, *args, **kwargs):
        daily = get_object_or_404(ScheduleDaily, emp_no=emp_no, pk=pk)
        daily_serializer = ScheduleDailySerializer(daily, data=request.data)
        if daily_serializer.is_valid(raise_exception=True):
            daily_serializer.save()
            return Response(daily_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(daily_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Government Mandated Contribution
class TaxView(APIView):
    def get(self, request, emp_no=None, pk=None, *args, **kwargs):
        if emp_no is not None:
            tax = get_object_or_404(Tax, emp_no=emp_no)
            tax_serializer = TaxSerializer(tax)
            return Response(tax_serializer.data, status=status.HTTP_200_OK)
        tax = Tax.objects.all()
        tax_serializer = TaxSerializer(tax, many=True)
        return Response(tax_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        tax_serializer = TaxSerializer(data=request.data)
        if tax_serializer.is_valid(raise_exception=True):
            tax_serializer.save()
            return Response(tax_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(tax_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None, *args, **kwargs):
        tax = get_object_or_404(Tax, pk=pk)
        tax_serializer = TaxSerializer(tax, data=request.data)
        if tax_serializer.is_valid(raise_exception=True):
            tax_serializer.save()
            return Response(tax_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(tax_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PagibigView(APIView):
    def get(self, request, emp_no=None, *args, **kwargs):
        if emp_no is not None:
            pagibig = get_object_or_404(PAGIBIG, emp_no=emp_no)
            pagibig_serializer = PAGIBIGSerializer(pagibig)
            return Response(pagibig_serializer.data, status=status.HTTP_200_OK)
        pagibig = PAGIBIG.objects.all()
        pagibig_serializer = PAGIBIGSerializer(pagibig, many=True)
        return Response(pagibig_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        pagibig_serializer = PAGIBIGSerializer(data=request.data)
        if pagibig_serializer.is_valid(raise_exception=True):
            pagibig_serializer.save()
            return Response(pagibig_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(pagibig_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, emp_no=None, *args, **kwargs):
        pagibig = get_object_or_404(PAGIBIG, emp_no=emp_no)
        pagibig_serializer = PAGIBIGSerializer(pagibig, data=request.data)
        if pagibig_serializer.is_valid(raise_exception=True):
            pagibig_serializer.save()
            return Response(pagibig_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(pagibig_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SssView(APIView):
    def get(self, request, emp_no=None, *args, **kwargs):
        if emp_no is not None:
            sss = get_object_or_404(SSS, emp_no=emp_no)
            sss_serializer = SSSSerializer(sss)
            return Response(sss_serializer.data, status=status.HTTP_200_OK)
        sss = SSS.objects.all()
        sss_serializer = SSSSerializer(sss, many=True)
        return Response(sss_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        sss_serializer = SSSSerializer(data=request.data)
        if sss_serializer.is_valid(raise_exception=True):
            sss_serializer.save()
            return Response(sss_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(sss_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, emp_no=None, *args, **kwargs):
        sss = get_object_or_404(SSS, emp_no=emp_no)
        sss_serializer = SSSSerializer(sss, data=request.data)
        if sss_serializer.is_valid(raise_exception=True):
            sss_serializer.save()
            return Response(sss_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(sss_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhilhealthView(APIView):
    def get(self, request, emp_no=None, *args, **kwargs):
        if emp_no is not None:
            philhealth = get_object_or_404(Philhealth, emp_no=emp_no)
            philhealth_serializer = PhilhealthSerializer(philhealth)
            return Response(philhealth_serializer.data, status=status.HTTP_200_OK)
        philhealth = Philhealth.objects.all()
        philhealth_serializer = PhilhealthSerializer(philhealth, many=True)
        return Response(philhealth_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        philhealth_serializer = PhilhealthSerializer(data=request.data)
        if philhealth_serializer.is_valid(raise_exception=True):
            philhealth_serializer.save()
            return Response(philhealth_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(philhealth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, emp_no=None, *args, **kwargs):
        philhealth = get_object_or_404(Philhealth, emp_no=emp_no)
        philhealth_serializer = PhilhealthSerializer(philhealth, data=request.data)
        if philhealth_serializer.is_valid(raise_exception=True):
            philhealth_serializer.save()
            return Response(philhealth_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(philhealth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
        if emp_no is not None:
            dtr_summary = DTRSummary.objects.filter(emp_no=emp_no)
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
        
    def post(self, request, *args, **kwargs):
        cutoff_serializer = CutoffSerializer(data=request.data)
        if cutoff_serializer.is_valid(raise_exception=True):
            cutoff_serializer.save()
            return Response(cutoff_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(cutoff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None, *args, **kwargs):
        cutoff = get_object_or_404(Cutoff, pk=pk)
        cutoff_serializer = CutoffSerializer(cutoff, data=request.data)
        if cutoff_serializer.is_valid(raise_exception=True):
            cutoff_serializer.save()
            return Response(cutoff_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(cutoff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        # elif user_emp_nos == None:
        #     return Response({"Error Message": "Select at least one (1) Employee from the list"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            employees = Employee.objects.filter(payroll_group_code=payroll_group_code, date_deleted=None)        
            response = merge_dtr_entries(employees, cutoff_code, operation="null")

            return response        
    
class DTRCutoffSummaryView(APIView):
    def get(self, request, emp_no=None, *args, **kwargs):
        if emp_no is not None:
            dtr_cutoff = DTRCutoff.objects.filter(emp_no=emp_no, date_deleted__isnull=True)
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
        return Response({"Message": f"DTR Cutoff Summary ID {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
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
        # elif user_emp_nos == None:
        #     return Response({"Error Message": "Select at least one (1) Employee from the list"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            employees = Employee.objects.filter(payroll_group_code=payroll_group_code, date_deleted=None)
            operation = "null"
            response = create_dtr_cutoff_summary(employees, cutoff_code, cutoff_start_date, cutoff_end_date, operation)
            return Response
          
    


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
        is_disabled_loan = request.data['is_disabled_loan']
        is_ca = request.data['is_ca']
        is_pagibig_house = request.data['is_pagibig_house']
        is_pagibig_cal = request.data['is_pagibig_cal']
        is_pagibig_cash = request.data['is_pagibig_cash']
        is_sss_cal = request.data['is_sss_cal']
        is_sss_cash = request.data['is_sss_cash']
        is_disabled_deduction = request.data['is_disabled_deduction']
        is_30 = request.data['is_30']
        is_70 = request.data['is_70']

        user_emp_nos = request.data['emp_no']
        cutoff_code = request.data['cutoff_code']
        cutoff = Cutoff.objects.get(pk=cutoff_code)
        if user_emp_nos:
            employees = Employee.objects.filter(emp_no__in=user_emp_nos, payroll_group_code=cutoff.payroll_group_code, date_deleted=None)
            response = create_payroll(employees, cutoff, is_disabled_loan, is_ca, is_pagibig_house, is_pagibig_cal, is_pagibig_cash, is_sss_cal, is_sss_cash, is_disabled_deduction, is_30, is_70, operation="list")

            return response
        
        # elif user_emp_nos == None:
        #     return Response({"Error Message": "Select at least one (1) Employee from the list"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            employees = Employee.objects.filter(payroll_group_code=cutoff.payroll_group_code, date_deleted=None)
            response = create_payroll(employees, cutoff, is_disabled_loan, is_ca, is_pagibig_house, is_pagibig_cal, is_pagibig_cash, is_sss_cal, is_sss_cash, is_disabled_deduction, is_30, is_70, operation="null")

            return response

class CashAdvanceView(APIView):
    def get(self, request, *args, **kwargs):
        emp_no = request.data['emp_no'] if request.data['emp_no'] else None
        if emp_no is not None:
            ca = CashAdvance.objects.filter(emp_no=emp_no)
            ca_serializer = CashAdvanceSerializer(ca, many=True)
            return Response(ca_serializer.data, status=status.HTTP_200_OK)
        ca = CashAdvance.objects.all()
        ca_serializer = CashAdvanceSerializer(ca, many=True)
        return Response(ca_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        ca_serializer = CashAdvanceSerializer(data=request.data)
        if ca_serializer.is_valid(raise_exception=True):
            ca_serializer.save()
            return Response(ca_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ca_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None, *args, **kwargs):
        ca = get_object_or_404(CashAdvance, pk=pk)
        ca_serializer = CashAdvanceSerializer(ca, data=request.data)
        if ca_serializer.is_valid(raise_exception=True):
            ca_serializer.save()
            return Response(ca_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(ca_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AllowanceTypeView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            allowance_type = get_object_or_404(AllowanceType, pk=pk, date_deleted__isnull=True)
            allowance_type_serializer = AllowanceTypeSerializer(allowance_type)
            return Response(allowance_type_serializer.data, status=status.HTTP_200_OK)
        allowance_type = AllowanceType.objects.filter(date_deleted__isnull=True)
        allowance_type_serializer = AllowanceTypeSerializer(allowance_type, many=True)
        return Response(allowance_type_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        allowance_type_serializer = AllowanceTypeSerializer(data=request.data)
        if allowance_type_serializer.is_valid(raise_exception=True):
            allowance_type_serializer.save()
            return Response(allowance_type_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(allowance_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None, *args, **kwargs):
        allowance_type = get_object_or_404(AllowanceType, pk=pk, date_deleted__isnull=True)
        allowance_type_serializer = AllowanceTypeSerializer(allowance_type, data=request.data)
        if allowance_type_serializer.is_valid(raise_exception=True):
            allowance_type_serializer.save()
            return Response(allowance_type_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(allowance_type_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        allowance_type = get_object_or_404(AllowanceType, pk=pk, date_deleted__isnull=True)
        allowance_type.date_deleted = datetime.now()
        allowance_type.save()
        return Response({"Message": f"Allowance Type ID {pk} successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class AllowanceEntryView(APIView):
    def get(self, request, *args, **kwargs):
        emp_no = request.data['emp_no']
        if emp_no is not None:
            allowance_entry = AllowanceEntry.objects.filter(emp_no=emp_no, date_deleted__isnull=True)
            allowance_entry_serializer = AllowanceEntrySerializer(allowance_entry, many=True)
            return Response(allowance_entry_serializer.data, status=status.HTTP_200_OK)
        allowance_entry = AllowanceEntry.objects.filter(date_deleted__isnull=True)
        allowance_entry_serializer = AllowanceEntrySerializer(allowance_entry, many=True)
        return Response(allowance_entry_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        allowance_entry_serializer = AllowanceEntrySerializer(data=request.data)
        if allowance_entry_serializer.is_valid(raise_exception=True):
            allowance_entry_serializer.save()
            return Response(allowance_entry_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(allowance_entry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None, *args, **kwargs):
        allowance_entry = get_object_or_404(AllowanceEntry, pk=pk, date_deleted__isnull=True)
        allowance_entry_serializer = AllowanceEntrySerializer(allowance_entry, data=request.data)
        if allowance_entry_serializer.is_valid(raise_exception=True):
            allowance_entry_serializer.save()
            return Response(allowance_entry_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(allowance_entry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk=None, *args, **kwargs):
        allowance_entry = get_object_or_404(AllowanceEntry, pk=pk, date_deleted__isnull=True)
        allowance_entry.date_deleted = datetime.now()
        allowance_entry.save()
        return Response({"Message": f"Allowance Entry ID {pk} successfully deleted"})

class TaxColletedView(APIView):
    def get(self, request, *args, **kwargs):
        emp_no = request.data['emp_no']
        if emp_no is not None:
            tax_collected = TaxCollected.objects.filter(emp_no=emp_no)
            tax_collected_serializer = TaxCollectedSerializer(tax_collected, many=True)
            return Response(tax_collected_serializer.data, status=status.HTTP_200_OK)
        tax_collected = TaxCollected.objects.all()
        tax_collected_serializer = TaxCollectedSerializer(tax_collected, many=True)
        return Response(tax_collected_serializer.data, status=status.HTTP_200_OK)
    
class Pay13THView(APIView):
    def get(self, request, *args, **kwargs):
        emp_no = request.data['emp_no']
        if emp_no is not None:
            pay13 = Pay13TH.objects.filter(emp_no=emp_no)
            pay13_serializer = Pay13THSerializer(pay13, many=True)
            return Response(pay13_serializer.data, status=status.HTTP_200_OK)
        pay13 = Pay13TH.objects.all()
        pay13_serializer = Pay13THSerializer(pay13, many=True)
        return Response(pay13_serializer.data, status=status.HTTP_200_OK)
    
class Create13THPayView(APIView):
    def post(self, request, *args, **kwargs):
        emp_nos = request.data['emp_no']
        for emp_no in emp_nos:
            payrolls = Payroll.objects.filter(emp_no=emp_no)
            employee = get_object_or_404(Employee,emp_no=emp_no)
            total_gross_pay = 0
            date_from = payrolls.first().pr_cutoff_code.co_date_from
            date_to = payrolls.last().pr_cutoff_code.co_date_to
            count = payrolls.count()
            for payroll in payrolls:
                total_gross_pay += payroll.gross_pay
                print(payroll.gross_pay)

            total_13_pay = total_gross_pay/count

            pay13th = {
                "coverage_from": date_from,
                "coverage_to": date_to,
                "total_pay": total_13_pay,
                "emp_no": employee.emp_no
            }

            pay13th_serializer = Pay13THSerializer(data=pay13th)
            if pay13th_serializer.is_valid(raise_exception=True):
                pay13th_serializer.save()
                return Response(pay13th_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(pay13th_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"Message": "Sample 13th month pay"}, status=status.HTTP_200_OK)

    
class AnnouncementView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            announcement = get_object_or_404(Announcement, pk=pk)
            announcement_serializer = AnnouncementSerializer(announcement)
            return Response(announcement_serializer.data, status=status.HTTP_200_OK)
        announcement = Announcement.objects.all()
        announcement_serializer = AnnouncementSerializer(announcement,many=True)
        return Response(announcement_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        announcement_serializer = AnnouncementSerializer(data=request.data)
        if announcement_serializer.is_valid(raise_exception=True):
            announcement_serializer.save()
            return Response(announcement_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(announcement_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None, *args, **kwargs):
        announcement = get_object_or_404(Announcement, pk=pk)
        announcement_serializer = AnnouncementSerializer(announcement, data=request.data)
        if announcement_serializer.is_valid(raise_exception=True):
            announcement_serializer.save()
            return Response(announcement_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(announcement_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# Asset
class AssetsListView(APIView):
    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            asset_list = get_object_or_404(AssetsLists, pk=pk)
            asset_list_serializer = AssestsListSerializer(asset_list)
            return Response(asset_list_serializer.data, status=status.HTTP_200_OK)
        asset_list = AssetsLists.objects.all()
        asset_list_serializer = AssestsListSerializer(asset_list, many=True)
        return Response(asset_list_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        asset_list_serializer = AssestsListSerializer(data=request.data)
        if asset_list_serializer.is_valid(raise_exception=True):
            asset_list_serializer.save()
            return Response(asset_list_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(asset_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None, *args, **kwargs):
        asset_list = get_object_or_404(AssetsLists, pk=pk)
        asset_list_serializer = AssestsListSerializer(asset_list, data=request.data)
        if asset_list_serializer.is_valid(raise_exception=True):
            asset_list_serializer.save()
            return Response(asset_list_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(asset_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AssetsAccountView(APIView):
    def get(self, request, *args, **kwargs):
        emp_no = request.data['emp_no']
        if emp_no is not None:
            account = AssetsAccount.objects.filter(assigned_to=emp_no)
            account_serializer = AssetsAccountSerializer(account, many=True)
            return Response(account_serializer.data, status=status.HTTP_200_OK)
        account = AssetsAccount.objects.all()
        account_serializer = AssetsAccountSerializer(account, many=True)
        return Response(account_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        account_serializer = AssetsAccountSerializer(data=request.data)
        if account_serializer.is_valid(raise_exception=True):
            account_serializer.save()
            return Response(account_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None, *args, **kwargs):
        account = get_object_or_404(AssetsAccount, pk=pk)
        account_serializer = AssetsAccountSerializer(account, data=request.data)
        if account_serializer.is_valid(raise_exception=True):
            account_serializer.save()
            return Response(account_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TestTSVUploadView(APIView):
    def post(self, request, *args, **kwargs):
        tsv_file = request.FILES.get('file')
        tsv_filename = str(tsv_file)

        if not tsv_file:
            return Response({"message": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)    
        else:
            if tsv_filename.endswith(".tsv"):
                response = newest_dtr_logs_upload(tsv_file)
                return response
            else:
                return Response({"Message": "The file you uploaded cannot be processed due to incorrect file extension"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)                
            
class TestMergeDTRSummaryView(APIView):
    def post(self, request, *args, **kwargs):
        user_emp_nos = request.data["emp_no"]
        cutoff_code = request.data["cutoff_code"]
        cutoff = get_object_or_404(Cutoff, pk=cutoff_code)
        payroll_group_code = cutoff.payroll_group_code

        if user_emp_nos:
            employees = Employee.objects.filter(emp_no__in=user_emp_nos, payroll_group_code=payroll_group_code, date_deleted=None)            
            response = new_merge_dtr_entries(employees, cutoff_code, operation="list")

            return response

        else:
            employees = Employee.objects.filter(payroll_group_code=payroll_group_code, date_deleted=None)        
            response = new_merge_dtr_entries(employees, cutoff_code, operation="null")

            return response 
