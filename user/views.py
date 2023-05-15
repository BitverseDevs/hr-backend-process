from django.shortcuts import render, get_object_or_404

from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from user.models import Branch, Department, Division, PayrollGroup, Position, Rank, Tax, Province, CityMunicipality, PAGIBIG, SSS, Philhealth, Employee, User, AuditTrail, DTR, DTRSummary, Holiday, OBT, Overtime, Leaves, Adjustment, Cutoff, Schedule
from user.serializers import BranchSerializer, DepartmentSerializer, DivisionSerializer, PayrollGroupSerializer, PositionSerializer, RankSerializer, TaxSerializer, ProvinceSerializer, CityMunicipalitySerializer, PAGIBIGSerializer, SSSSerializer, PhilhealthSerializer, EmployeeSerializer, UserSerializer, AuditTrailSerializer, DTRSerializer, DTRSummarySerializer, HolidaySerializer, OBTSerializer, OvertimeSerializer, LeavesSerializer, AdjustmentSerializer,CutoffSerializer, ScheduleSerializer

import secret, datetime, jwt, csv

@api_view(['GET', 'POST'])
def PhilhealthView(request):
    if request.method == 'GET':
        philhealth = Schedule.objects.all()
        serializer = ScheduleSerializer(philhealth, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request.data)
        serializer = PhilhealthSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @staticmethod
    def post(request):
        username = request.data["username"]
        password = request.data["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            user.failed_login_attempts += 1
            user.save()
            raise AuthenticationFailed("Incorrect password!")
        
        user.last_login = datetime.datetime.now()
        user.save()
        user_serializer = UserSerializer(user)

        employee = get_object_or_404(Employee, employee_number=user_serializer.data["employee_number"])
        employee_serializer = EmployeeSerializer(employee)

        payload = {
            "id": user.id,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.now()
        }
        token = jwt.encode(payload=payload, key=secret.JWT_SECRET, algorithm="HS256")
        data = {
            "jwt": token,
            "user": user_serializer.data,
            "employee_detail": employee_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    
class EmployeesListView(APIView):
    def get(self, request):
        employees = Employee.objects.filter(date_deleted__exact=None)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployeesPagination(PageNumberPagination):
    page_size = 50
    # page_size_query_param = 'page_size'
    max_page_size = 100

class EmployeesView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = EmployeesPagination

    def get(self, request, employee_number=None):
        if employee_number is not None:
            employee = get_object_or_404(Employee, employee_number=employee_number, date_deleted__isnull=True)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            employees = Employee.objects.filter(date_deleted__exact=None)
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(employees, request)
            serializer = EmployeeSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data) if result_page is not None else Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, employee_number):
        employee = get_object_or_404(Employee, employee_number=employee_number)
        serializer = EmployeeSerializer(employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, employee_number):
        employee = get_object_or_404(Employee, employee_number=employee_number)
        employee.date_deleted = datetime.date.today()
        employee.save()
        
        return Response({"message": "Account successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

class BirthdayView(APIView):
    def get(self, request):
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
    def get(self, request):
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
    
class TsvFileUploadView(APIView):

    def post(self, request, *args, **kwargs):
        tsv_file = request.FILES.get('file')
        print(tsv_file)

        if not tsv_file:
            return Response({"error": "No TSV file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tsv_file_text = tsv_file.read().decode('utf-8')
            reader = csv.reader(tsv_file_text.splitlines(), delimiter='\t')
            for row in reader:
                dtr = DTR.objects.create(
                    bio_id = row[0],
                    datetime_bio = row[1],
                    flag1_in_out = 1 if (row[3] == 1) else 0,
                    flag2_lout_lin = 1 if (row[5] == 1) else 0,
                    entry_type = 1 if row[3] == 1 else 0,
                    branch_code = Branch.objects.get(branch_name=row[6]),
                    employee_number = Employee.objects.get(employee_number=row[0])
                )
                dtr.save()      
            return Response({"message": "Successfully uploaded DTR logs to DTR Model"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


