from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from user.models import Branch, Department, Division, PayrollGroup, Position, Rank, Tax, Province, CityMunicipality, PAGIBIG, SSS, Philhealth, Employee, User, AuditTrail, DTR, DTRSummary, DTRCutoff, Holiday, OBT, Overtime, Leaves, LeavesCredit, LeavesType, Adjustment, Cutoff, ScheduleShift, ScheduleDaily, UnaccountedAttendance, Payroll
from user.serializers import BranchSerializer, DepartmentSerializer, DivisionSerializer, PayrollGroupSerializer, PositionSerializer, RankSerializer, TaxSerializer, ProvinceSerializer, CityMunicipalitySerializer, PAGIBIGSerializer, SSSSerializer, PhilhealthSerializer, EmployeeSerializer, UserSerializer, AuditTrailSerializer, DTRSerializer, DTRSummarySerializer, DTRCutoffSerializer, HolidaySerializer, OBTSerializer, OvertimeSerializer, LeavesSerializer, LeavesCreditSerializer, LeavesTypeSerializer, AdjustmentSerializer,CutoffSerializer, ScheduleShiftSerializer, ScheduleDailySerializer, UnaccountedAttendanceSerializer, SpecificEmployeeSerializer, PayrollSerializer

import secret, jwt, csv, pandas as pd, io
from datetime import datetime, timedelta, time, date

from user.dtr_process import merge_dtr_entries, create_dtr_cutoff_summary

# Test API

@api_view(['GET', 'POST'])
def test_view(request, pk=None, *args, **kwargs):
    if request.method == 'GET':
        if pk is not None:
            test = get_object_or_404(UnaccountedAttendance, pk=pk)
            serializer = UnaccountedAttendanceSerializer(test)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            test = UnaccountedAttendance.objects.all()
            serializer = UnaccountedAttendanceSerializer(test, many=True)
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
    def post(self, request, *args, **kwargs):
        
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
        employee = get_object_or_404(Employee, emp_no=emp_no)
        employee.date_deleted = date.today()
        employee.save()
        
        return Response({"message": "Account successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

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
        

# Employee Upload CSV

class EmployeeUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        filename = str(file)
        existing = []
        non_existing = []

        if not file:
            return Response({"Message": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            if filename.endswith('.csv'):
                csv_file = file.read().decode('utf-8')
                reader = csv.reader(csv_file.splitlines(),delimiter=',')

                for row in reader:
                    emp_no = row[0]

                    if Employee.objects.filter(emp_no=emp_no).exists():
                        existing.append(row)
                        continue

                    else:
                        gender = {
                            "Male": "M",
                            "Female": "F"
                        }

                        civil_status = {
                            "Single": "S",
                            "Married": "M",
                            "Annulled": "A",
                            "Widowed": "W",
                            "Separated": "SA"
                        }
                        
                        employee = {
                            "emp_no": row[0],
                            "first_name": row[1],
                            "middle_name": None if row[2] == "" else row[2],
                            "last_name": row[3],
                            "suffix": None if row[4] == "" else row[4],
                            "birthday": row[5],
                            "birth_place": row[6],
                            "civil_status": civil_status[row[7]] if row[7] in civil_status.keys() else row[7],
                            "gender": gender[row[8]] if row[8] in gender.keys() else row[8],
                            "address": row[9],
                            "provincial_address": None if row[10] == "" else row[10],
                            "mobile_phone": row[11],
                            "email_address": f"{row[1].lower()}.{row[3].replace(' ', '_').lower()}@sample.com",
                            "date_hired": row[12],
                            "date_resigned": None,
                            "date_added": datetime.now(),
                            "date_deleted": None,                            
                        }

                        serializer = EmployeeSerializer(data=employee)

                        if serializer.is_valid():
                            serializer.save()
                            non_existing.append(row)

                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                if existing:
                    return Response({
                        "Message": "Uploaded employee data contains employee number that already exists in the sysyem. Unique employee data is successfully uploaded in the database", 
                        "Existing employee/s": existing, 
                        "Unique employee/s": non_existing
                        }, status=status.HTTP_200_OK)
            
                elif not existing:
                    return Response({
                        "Message": "All employee data is unique and is successfully uploaded into the database",
                        "Unique employee/s": non_existing
                    }, status=status.HTTP_202_ACCEPTED)

            else:                
                return Response({"Message": "The file you uploaded cannot be processed due to incorrect file extension"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)            
            

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
            return Response({"message": "No file uploaded"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        
        else:
            if tsv_filename.endswith(".tsv"):
                try:
                    stream = io.StringIO(tsv_file.read().decode('utf-8'))
                    columns = ['bio_id', 'datetime_bio', 'duty_in', 'duty_out', 'lunch_in', 'lunch_out', 'branch']
                    dframe = pd.read_table(stream, header=None, names=columns)
                    dframe = dframe.sort_values(['bio_id', 'datetime_bio'])
                    dframe['datetime_bio'] = pd.to_datetime(dframe['datetime_bio'])
                    dframe['date'] = dframe["datetime_bio"].dt.date
                    dframe['bio_id'] = dframe['bio_id'].astype(int)
                    grouped_df = dframe.groupby(['bio_id', 'date']).agg(datetime_bio_min=("datetime_bio", "min"), datetime_bio_max=("datetime_bio", "max")).reset_index()
                    grouped_df['branch'] = dframe['branch']
                    ids = grouped_df['bio_id'].unique()

                    for id in ids:
                        select_row = grouped_df[grouped_df['bio_id'] == id]
                        employee = Employee.objects.get(bio_id=id)

                        for i in range(len(select_row)):
                            duty_in = select_row.iloc[i]['datetime_bio_min']
                            duty_out = select_row.iloc[i]['datetime_bio_max']
                            branch = select_row.iloc[i]['branch']
                            date = select_row.iloc[i]['date']
                            emp_branch = Branch.objects.get(branch_name=branch)                        
                            schedule = ScheduleDaily.objects.get(emp_no=employee.emp_no, business_date=date)

                            dtr_in = {
                                'emp_no': employee.emp_no,
                                'bio_id': employee.bio_id,
                                'datetime_bio': duty_in,
                                'flag1_in_out': 0,
                                'entry_type': "DIN",
                                'date_uploaded': datetime.now(),
                                'branch_code': emp_branch.pk,
                                'schedule_daily_code': schedule.pk
                            }

                            dtr_out = {
                                'emp_no': employee.emp_no,
                                'bio_id': employee.bio_id,
                                'datetime_bio': duty_out,
                                'flag1_in_out': 1,
                                'entry_type': "DOUT",
                                'date_uploaded': datetime.now(),
                                'branch_code': emp_branch.pk,
                                'schedule_daily_code': schedule.pk
                            }

                            dtr_in_serializer = DTRSerializer(data=dtr_in)
                            dtr_out_serializer = DTRSerializer(data=dtr_out)

                            if dtr_in_serializer.is_valid():
                                dtr_in_serializer.save()
                            else:
                                return Response({"message": "DTR IN", "error": dtr_in_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                            
                            if dtr_out_serializer.is_valid():
                                dtr_out_serializer.save()
                            else:
                                return Response({"message": "DTR OUT", "error": dtr_out_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

                    return Response({"message": "Successfully uploaded to DTR database"}, status=status.HTTP_201_CREATED)
                
                except Exception as e:
                    return Response({"Overall error": str(e)}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            else:
                return Response({"Message": "The file you uploaded cannot be processed due to incorrect file extension"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)                


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
        start_date = cutoff.co_date_from
        end_date = cutoff.co_date_to
        delta = timedelta(days=1)

        if user_emp_nos:
            employees = Employee.objects.filter(emp_no__in=user_emp_nos, payroll_group_code=payroll_group_code, date_deleted=None)
            operation = "list"
            response = merge_dtr_entries(employees, cutoff_code, start_date, end_date, delta, operation)

            return response

        else:
            employees = Employee.objects.filter(payroll_group_code=payroll_group_code, date_deleted=None)
            operation = "null"
            response = merge_dtr_entries(employees, cutoff_code, start_date, end_date, delta, operation)

            return response
        

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
            operation = "null"
            response = create_dtr_cutoff_summary(employees, cutoff_code, cutoff_start_date, cutoff_end_date, operation)

            return response            
        

class DTRSummaryView(APIView):
    def get(self, request, emp_no=None, cutoff_code=None, *args, **kwargs):
        if emp_no is None:
            dtr_summary = DTRSummary.objects.all()
            dtr_summary_serializer = DTRSummarySerializer(dtr_summary, many=True)
            return Response(dtr_summary_serializer.data, status=status.HTTP_200_OK)            
        
        employee = get_object_or_404(Employee, emp_no=emp_no, date_deleted__exact=None)
        cutoff_code = request.data['cutoff_code']
        if cutoff_code is not None:    
            cutoff = get_object_or_404(Cutoff, pk=cutoff_code)            
            date_from = cutoff.co_date_from
            date_to = cutoff.co_date_to
            dtr_summary = DTRSummary.objects.filter(emp_no=employee.emp_no, business_date__gte=date_from, business_date__lte=date_to).order_by('-business_date')
            dtr_summary_serializer = DTRSummarySerializer(dtr_summary, many=True)
            return Response(dtr_summary_serializer.data, status=status.HTTP_200_OK)
        
        dtr_summary = DTRSummary.objects.filter(emp_no=employee.emp_no).order_by('-business_date')
        dtr_summary_serializer = DTRSummarySerializer(dtr_summary, many=True)
        return Response(dtr_summary_serializer.data, status=status.HTTP_200_OK)
    
class DTRCutoffSummaryView(APIView):
    def get(self, request, emp_no=None, *args, **kwargs):
        if emp_no is None:
            dtr_cutoff_summary = DTRCutoff.objects.all()
            dtr_cutoff_summary_serializer = DTRCutoffSerializer(dtr_cutoff_summary, many=True)
            return Response(dtr_cutoff_summary_serializer.data, status=status.HTTP_200_OK) 
        
        employee = get_object_or_404(Employee, emp_no=emp_no, date_deleted__exact=None)
        cutoff_code = request.data['cutoff_code']
        if cutoff_code is not None:    
            cutoff = get_object_or_404(Cutoff, pk=cutoff_code)            
            date_from = cutoff.co_date_from
            date_to = cutoff.co_date_to
            dtr_cutoff_summary = DTRCutoff.objects.filter(emp_no=employee.emp_no, business_date_from__gte=date_from, business_date_to__lte=date_to)
            dtr_cutoff_summary_serializer = DTRCutoffSerializer(dtr_cutoff_summary, many=True)
            return Response(dtr_cutoff_summary_serializer.data, status=status.HTTP_200_OK)
        
        dtr_cutoff_summary = DTRCutoff.objects.filter(emp_no=employee.emp_no)
        dtr_cutoff_summary_serializer = DTRCutoffSerializer(dtr_cutoff_summary, many=True)
        return Response(dtr_cutoff_summary_serializer.data, status=status.HTTP_200_OK)
    

class PayrollView(APIView):
    def get(self, request, *args, **kwargs):
        payrolls = Payroll.objects.all()
        serializer = PayrollSerializer(payrolls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreatePayrollView(APIView):
    def post(self, request, *args, **kwargs):
        cutoff_code = request.data['cutoff_code']
        user_emp_nos = request.data['emp_no']

        if user_emp_nos:
            for user_emp_no in user_emp_nos:
                try:                                       
                    employee = Employee.objects.get(emp_no=user_emp_no)
                    cutoff = get_object_or_404(Cutoff, pk=cutoff_code)
                    pagibig = get_object_or_404(PAGIBIG, emp_no=employee.emp_no)
                    tax = get_object_or_404(Tax, emp_no=employee.emp_no)
                    sss = get_object_or_404(SSS, emp_no=employee.emp_no)
                    philhealth = get_object_or_404(Philhealth, emp_no=employee.emp_no)
                    dtr_cutoff = DTRCutoff.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff.pk).first()

                    fname = employee.first_name.upper()
                    mname = employee.middle_name.upper() if employee.middle_name else ""
                    lname = employee.last_name.upper()
                    suffix = employee.suffix.upper() if employee.suffix else ""

                    if mname and suffix:
                        cname = f"{fname} {mname} {lname} {suffix}"                    
                    elif mname:
                        cname = f"{fname} {mname} {lname}"
                    elif suffix:
                        cname = f"{fname} {lname} {suffix}"
                    else:
                        cname = f"{fname} {lname}"
                    
                    run_date = datetime.now()
                    accnt_no = employee.accnt_no if employee.accnt_no else ""
                    salary_basic = employee.emp_salary_basic if employee.emp_salary_basic else 0.00
                    salary_allowance = employee.emp_salary_allowance if employee.emp_salary_allowance else 0.00
                    salary_other = employee.emp_salary_other if employee.emp_salary_other else 0.00
                    salary_type = employee.emp_salary_type
                    gross_pay = salary_basic + salary_allowance + salary_other
                    work_days_total = cutoff.reg_days_total

                    if salary_type == "daily":
                        daily_salary_basic = salary_basic
                        daily_salary_allowance = salary_allowance
                        daily_salary_other = salary_other
                    else:
                        daily_salary_basic = salary_basic/work_days_total
                        daily_salary_allowance = salary_allowance/work_days_total if salary_allowance != 0 else 0
                        daily_salary_other = salary_other/work_days_total if salary_other != 0 else 0

                    daily_total = daily_salary_basic + daily_salary_allowance + daily_salary_other
                    daily_salary_basic_hour = daily_salary_basic/8
                    daily_salary_basic_minute = daily_salary_basic_hour/60

                    leaves_amount = dtr_cutoff.paid_leaves_total * (daily_total)
                    ot_amount = dtr_cutoff.reg_ot_total * (daily_salary_basic_hour * 1.1)
                    holiday_amount = (dtr_cutoff.reg_holiday_total + dtr_cutoff.sp_holiday_total) * daily_total 
                    nd_amount = 0.00

                    lates_amount = dtr_cutoff.lates_total * daily_salary_basic_minute
                    utime_amount = dtr_cutoff.undertime_total * daily_salary_basic_minute
                    absent_amount = dtr_cutoff.absent_total * daily_salary_basic

                    sss_contribution = sss.sss_contribution_month
                    sss_cashloan = sss.sss_with_cashloan_amount
                    sss_calloan = sss.sss_with_calloan_amount

                    pagibig_contribution = pagibig.pagibig_contribution_month
                    pagibig_cloan = pagibig.pagibig_with_cloan_amount
                    pagibig_hloan = pagibig.pagibig_with_hloan_amount

                    philhealth_contribution = philhealth.ph_contribution_month

                    cash_advance = 0.00
                    insurance = employee.insurance_life
                    other_deduction = employee.other_deductible

                    tax_amount = 0.00
                    additions = leaves_amount + ot_amount + holiday_amount + nd_amount
                    deductions = lates_amount + utime_amount + absent_amount + sss_contribution + sss_cashloan + sss_calloan + pagibig_contribution + pagibig_cloan + pagibig_hloan + philhealth_contribution + cash_advance + insurance + other_deduction
                    
                    initial_net_pay = gross_pay + additions - deductions
                    net_pay = initial_net_pay - tax_amount

                    payroll = {
                        "pr_cutoff_code": cutoff_code,
                        "emp_no": employee.emp_no,
                        'emp_cname': cname,
                        'run_date': run_date,
                        'accnt_no': accnt_no,
                        "salary_basic": salary_basic,
                        "salary_allowance": salary_allowance,
                        "salary_other": salary_other,
                        "salary_type": salary_type,
                        "gross_pay": gross_pay,
                        "work_days_total": work_days_total,
                        "daily_salary_basic": daily_salary_basic,
                        "daily_salary_allowance": daily_salary_allowance,
                        "daily_salary_other": daily_salary_other,
                        "leaves_amount_a": leaves_amount,
                        "ot_amount_a": ot_amount,
                        "holiday_amount_a": holiday_amount,
                        "nd_amount_a": nd_amount,
                        "lates_amount_d": lates_amount,
                        "utime_amount_d": utime_amount,
                        "absent_amount_d": absent_amount,
                        "tax_amount_d": tax_amount,
                        "sssc_amount_d": sss_contribution,
                        "sss_cashloan_d": sss_cashloan,
                        "sss_calloan_d": sss_calloan,
                        "pagibigc_amount_d": pagibig_contribution,
                        "pagibig_cloan_d": pagibig_cloan,
                        "pagibig_hloan_d": pagibig_hloan,
                        "cash_advance_amount_d": cash_advance,
                        "philhealthc_amount_d": philhealth_contribution,
                        "insurnace_d": insurance,
                        "other_d": other_deduction,
                        "net_pay": net_pay
                    }

                    return Response({"Message": "Testing Create Payroll", "Payroll": payroll}, status=status.HTTP_200_OK)

                except Exception as e:
                    return Response({"Exception Error": str(e)})

        return Response({"Message": "Testing Create Payroll"}, status=status.HTTP_200_OK)