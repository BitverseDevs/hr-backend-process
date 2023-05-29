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

import secret, jwt, csv, pandas as pd, io
from datetime import datetime, timedelta, time, date

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
                raise AuthenticationFailed("Incorrect password!")
            
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
        employee.date_deleted = date.today()
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
            reader = csv.reader(tsv_file.splitlines(), delimiter=',')
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
                    date_added = datetime.today(),
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
            return Response({"message": "No file uploaded"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        
        else:
            stream = io.StringIO(tsv_file.read().decode('utf-8'))
            dframe = pd.read_csv(stream)
            print(dframe)
            return Response({"message": "Test DTR Entry"})




























    # def post(self, request, *args, **kwargs):
    #     tsv_file = request.FILES.get('file')
    #     if not tsv_file:
    #         return Response({"error": "No TSV file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         tsv_file_text = tsv_file.read().decode('utf-8')
    #         reader = csv.reader(tsv_file_text.splitlines(), delimiter='\t')
    #         for row in reader:
    #             entry = ""
    #             if row[3] == "0" and row[5] == "0":
    #                 entry = "DIN"
    #             elif row[3] == "0" and row[5] == "1":
    #                 entry = "LOUT"
    #             elif row[3] == "1":
    #                 entry = "DOUT"

    #             employee = Employee.objects.get(bio_id=row[0])
    #             date = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S").date()
    #             sched = ScheduleDaily.objects.get(emp_no=employee.emp_no, business_date=date)
                # dtr = DTR(
                #     bio_id = employee,
                #     emp_no = employee,
                #     datetime_bio = row[1],
                #     flag1_in_out = int(row[3]),
                #     flag2_lout_lin = int(row[5]),
                #     entry_type = entry,
                #     date_uploaded = datetime.now(),

                #     branch_code = Branch.objects.get(branch_name=row[6]),
                #     schedule_daily_code = sched                
                # )
    #             serializer = DTRSerializer(dtr)
    #             content = JSONRenderer().render(serializer.data) 
    #             stream = io.BytesIO(content)
    #             data = JSONParser().parse(stream)
    #             dtr_serializer = DTRSerializer(data=data)
    #             if dtr_serializer.is_valid():
    #                 dtr_serializer.save()
    #                 continue
    #             else:
    #                 return Response({"error": dtr_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    #         return Response({"message": "Successfully uploaded to DTR database"}, status=status.HTTP_201_CREATED)
        
    #     except Exception as e:
    #         return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MergeDTREntryView(APIView):
    def post(self, request):
        user_emp_no = request.data["emp_no"]
        cutoff_code = request.data["cutoff_code"]

        if user_emp_no is not None:
            employee = get_object_or_404(Employee, emp_no=user_emp_no)
            cutoff = get_object_or_404(Cutoff, pk=cutoff_code)
            start_date = cutoff.co_date_from
            end_date = cutoff.co_date_to
            delta = timedelta(days=1)

            while start_date <= end_date:
                date_from = datetime(start_date.year, start_date.month, start_date.day)
                date_to = datetime(start_date.year, start_date.month, start_date.day, 23, 59, 59)
                dtr_entries = DTR.objects.filter(emp_no=employee.emp_no, datetime_bio__gte=date_from, datetime_bio__lte=date_to)

                if dtr_entries.exists():
                    business_date = dtr_entries.first().schedule_daily_code.business_date
                    shift_name = dtr_entries.first().schedule_daily_code.schedule_shift_code.name
                    duty_in = dtr_entries.first().datetime_bio
                    duty_out = dtr_entries.last().datetime_bio
                    sched_timein = dtr_entries.first().schedule_daily_code.schedule_shift_code.time_in
                    sched_timeout = dtr_entries.first().schedule_daily_code.schedule_shift_code.time_out
                    is_obt = False
                    is_ua = False
                    late = 0
                    undertime = 0
                    total_hours = 0
                    ot_total_hours = 0
                    curr_sched_timein = datetime(duty_in.year, duty_in.month, duty_in.day, sched_timein.hour, sched_timein.minute, sched_timein.second)
                    curr_sched_timeout = datetime(duty_out.year, duty_out.month, duty_out.day, sched_timeout.hour, sched_timeout.minute, sched_timeout.second)
                    timein_difference = duty_in - curr_sched_timein
                    timeout_difference = duty_out - curr_sched_timeout

                    print(f"Normal: {duty_in}")
                    print(f"Normal: {duty_out}")

                    if curr_sched_timein > duty_in or duty_out < curr_sched_timeout:
                        # create a loop for multiple obt or ua

                        # OBT
                        obts = OBT.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, obt_approval_status="APD", obt_date_from__gte=date_from, obt_date_to__lte=date_to)
                        if obts.exists():
                            is_obt = True
                            if obts.count == 2:
                                pass

                            else:
                                if obts.first().obt_date_to >= duty_out:
                                    duty_out = obts.first().obt_date_to
                                    print(duty_out)
                                    pass
                                elif obts.first().obt_date_from <= duty_in:
                                    duty_in = obts.first().obt_date_from
                                    print(duty_out)
                            
                            # for obt in obts:
                            #     if obt.obt_date_from < duty_in:
                            #         duty_in = obt.obt_date_from
                            #         print(f"OBT: {duty_in}")

                            #     if obt.obt_date_to < duty_out:
                            #         duty_out = obt.obt_date_to
                            #         print(f"OBT: {duty_out}")
                        
                        # Unaccounted Attendance
                        uas = UnaccountedAttendance.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, ua_approval_status="APD", ua_date_from__gte=date_from, ua_date_to__lte=date_to)
                        if uas.exists():
                            is_ua = True
                            for ua in uas:
                                if ua.ua_date_from < duty_in:
                                    duty_in = ua.ua_date_from                                    

                                if ua.ua_date_to < duty_out:
                                    duty_out = ua.ua_date_to                                    
                    
                    # Overtime 
                    ot = Overtime.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, ot_approval_status="APD", ot_date_from__gte=date_from, ot_date_to__lte=date_to)
                    if ot.exists():
                        ot_total_hours = ot.first().ot_date_to - ot.first().ot_date_from
                        ot_total_hours = ot_total_hours.seconds/60

                    # Lates, Undertime, Total hours

                    if timein_difference >= timedelta(minutes=0):
                        late = timein_difference.seconds/60

                    if timeout_difference >= timedelta(minutes=0):
                        undertime = timeout_difference.seconds/60
                    
                    work_hours = duty_out - duty_in
                    if work_hours >= timedelta(hours=8):
                        total_hours = 480
                    else:
                        total_hours = work_hours.seconds/60


                    dtr_summary = {
                        "emp_no": employee.emp_no,
                        "cutoff_code": cutoff_code,
                        "business_date": business_date,
                        "shift_name": shift_name,
                        "duty_in": duty_in,
                        "duty_out": duty_out,
                        "sched_timein": curr_sched_timein,
                        "sched_timeout": curr_sched_timeout,
                        "undertime": int(undertime),
                        "lates": int(late),
                        "total_hours": int(total_hours),
                        "reg_ot_total": int(ot_total_hours),
                        "nd_ot_total": 0,
                        "is_obt": is_obt,
                        "is_ua": is_ua
                    }

                    serializer = DTRSummarySerializer(data=dtr_summary)
                    if serializer.is_valid():
                        serializer.save()

                    else:
                        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                if not dtr_entries.exists():
                    pass

                start_date += delta

            return Response({"message": "Testing API"})
        
        else:
            pass