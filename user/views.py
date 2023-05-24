from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from user.models import Branch, Department, Division, PayrollGroup, Position, Rank, Tax, Province, CityMunicipality, PAGIBIG, SSS, Philhealth, Employee, User, AuditTrail, DTR, DTRSummary, DTRCutoff, Holiday, OBT, Overtime, Leaves, LeavesCredit, LeavesType, Adjustment, Cutoff, ScheduleShift, ScheduleDaily, UnaccountedAttendance
from user.serializers import BranchSerializer, DepartmentSerializer, DivisionSerializer, PayrollGroupSerializer, PositionSerializer, RankSerializer, TaxSerializer, ProvinceSerializer, CityMunicipalitySerializer, PAGIBIGSerializer, SSSSerializer, PhilhealthSerializer, EmployeeSerializer, UserSerializer, AuditTrailSerializer, DTRSerializer, DTRSummarySerializer, DTRCutoffSerializer, HolidaySerializer, OBTSerializer, OvertimeSerializer, LeavesSerializer, LeavesCreditSerializer, LeavesTypeSerializer, AdjustmentSerializer,CutoffSerializer, ScheduleShiftSerializer, ScheduleDailySerializer, UnaccountedAttendanceSerializer

import secret, datetime, jwt, csv, io

# Test API

@api_view(['GET', 'POST'])
def test_view(request, pk=None):
    if request.method == 'GET':
        if pk is not None:
            test = get_object_or_404(LeavesType, pk=pk)
            serializer = LeavesTypeSerializer(test)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            test = LeavesType.objects.all()
            serializer = LeavesTypeSerializer(test, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request.data)
        serializer = LeavesTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create new user based on existing employee data

class UserView(APIView):
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login Dashboard

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

        employee = get_object_or_404(Employee, emp_no=user_serializer.data["emp_no"])
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
    
# Employee Dashboard

class EmployeesView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, emp_no=None):
        if emp_no is not None:
            employee = get_object_or_404(Employee, emp_no=emp_no, date_deleted__isnull=True)
            serializer = EmployeeSerializer(employee)
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
        
    def put(self, request, emp_no):
        employee = get_object_or_404(Employee, emp_no=emp_no)
        serializer = EmployeeSerializer(employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, emp_no):
        employee = get_object_or_404(Employee, emp_no=emp_no)
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

class EmployeeUploadView(APIView):
    def post(self, request, *args, **kwargs):
        employee_file = request.FILES.get('file')

        if not employee_file:
            return Response({'message': "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tsv_file = employee_file.read().decode('utf-8')
            reader = csv.reader(tsv_file.splitlines(), delimiter='\t')
            for row in reader:
                employee = Employee.objects.create(
                    emp_no = row[0],
                    first_name = row[1],
                    middle_name = None if row[2] == "" else row[2],
                    last_name = row[3],
                    suffix = None if row[4] == "" else row[4],
                    birthday = row[5],
                    birth_place = row[6],
                    civil_status = 7,
                    gender = 8,
                    address = row[9],
                    provincial_address = None if row[10] == "" else row[10],
                    mobile_phone = row[11],
                    email_address = f"{row[1]}.{row[3]}@sample.com",
                    date_hired = row[12],
                    date_resigned = None,
                    approver = 0000,
                    date_added = datetime.datetime.today(),
                    date_deleted = None,
                )
            return Response({"message": "File has been read and successfully uploaded to Employee database"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ExportEmployeeView(APIView):
    def post(self, request, number_of_employee=None, order=None, *args, **kwargs):
        if number_of_employee is None and order is None:
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif number_of_employee is not None and order is None:
            employees = Employee.objects.all()[:number_of_employee]
            serializer = EmployeeSerializer(employees)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif order is not None and number_of_employee is None:
            employees = Employee.objects.order_by(order)
            serializer = EmployeeSerializer(employees)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif number_of_employee is not None and order is not None:
            employees = Employee.objects.order_by(order)[:number_of_employee]
            serializer = EmployeeSerializer(employees)
            return Response(serializer.data, status=status.HTTP_200_OK)

# DTR Dashboard

class DTRView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            dtr = get_object_or_404(DTR, pk=pk)
            serializer = DTRSerializer(dtr)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            dtr = DTR.objects.all()
            serializer = DTRSerializer(dtr)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class TsvFileUploadView(APIView):

    def post(self, request, *args, **kwargs):
        tsv_file = request.FILES.get('file')
        if not tsv_file:
            return Response({"error": "No TSV file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tsv_file_text = tsv_file.read().decode('utf-8')
            reader = csv.reader(tsv_file_text.splitlines(), delimiter='\t')
            for row in reader:
                entry = ""
                if row[3] == "0" and row[5] == "0":
                    entry = "DIN"
                elif row[3] == "0" and row[5] == "1":
                    entry = "LOUT"
                elif row[3] == "1":
                    entry = "DOUT"

                employee = Employee.objects.get(bio_id=row[0])
                date = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S").date()
                sched = ScheduleDaily.objects.get(emp_no=employee.emp_no, business_date=date)
                dtr = DTR(
                    bio_id = employee,
                    emp_no = employee,
                    datetime_bio = row[1],
                    flag1_in_out = int(row[3]),
                    flag2_lout_lin = int(row[5]),
                    entry_type = entry,
                    date_uploaded = datetime.datetime.now(),

                    branch_code = Branch.objects.get(branch_name=row[6]),
                    schedule_daily_code = sched                
                )
                serializer = DTRSerializer(dtr)
                content = JSONRenderer().render(serializer.data) 
                stream = io.BytesIO(content)
                data = JSONParser().parse(stream)
                dtr_serializer = DTRSerializer(data=data)
                if dtr_serializer.is_valid():
                    dtr_serializer.save()
                    continue
                else:
                    return Response({"error": dtr_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Successfully uploaded to DTR database"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MergeDTREntryView(APIView):
    def post(self, request):
        user = request.data["emp_no"]
        cutoff_code = request.data["cutoff_code"]

        if user is not None:
            dtrsummary = {}

            employee = Employee.objects.get(emp_no=request.data["emp_no"])
            cutoff = Cutoff.objects.get(pk=cutoff_code)
            dtr_entries = DTR.objects.filter(emp_no=employee.emp_no, datetime_bio__gte=cutoff.co_date_from, datetime_bio__lte=cutoff.co_date_to).order_by("schedule_daily_code", "datetime_bio")
            leaves = Leaves.objects.filter(Q(emp_no=employee.emp_no) & (Q(leave_date_approved1__isnull=False) | Q(leave_date_approved2__isnull=False)))
            ot = Overtime.objects.filter(Q(emp_no=employee.emp_no) & (Q(ot_date_approved1__isnull=False) | Q(ot_date_approved2__isnull=False)))
            obt = OBT.objects.filter(Q(emp_no=employee.emp_no) & (Q(obt_date_approved1__isnull=False) | Q(obt_date_approved2__isnull=False)))
            date = datetime.datetime(2023,5,31)
            holiday = Holiday.objects.get(holiday_date=date)
            ua = UnaccountedAttendance.objects.filter(Q(emp_no=employee.emp_no) & (Q(ua_date_approved1__isnull=False) | Q(ua_date_approved2__isnull=False)))
            print(holiday)
            for data in ua:
                print(data)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            # dtrs = DTR.objects.filter(emp_no=employee.emp_no, datetime_bio__gte=cutoff.co_date_from, datetime_bio__lte=cutoff.co_date_to).order_by("emp_no", "schedule_daily_code")
            
            # for dtr in dtrs:
            #     print(dtr.schedule_daily_code.business_date)

            # dtrsummary["emp_no"] = employee
            # dtrsummary["cutoff_code"] = cutoff
            # print(dtrsummary)

        elif user is None:
            pass

        return Response({"message": "Testing API"})