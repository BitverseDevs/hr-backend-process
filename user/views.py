from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from user.models import User, Employee, AuditTrail, DTR, DTRSummary, Holiday, OBT, Overtime, Leaves, Adjustment, Branch, Department, Division, Rank, Position, Province, CityMunicipality
from user.serializers import UserSerializer, EmployeeSerializer, AuditTrailSerializer, DTRSerializer, DTRSummarySerializer, HolidaySerializer, OBTSerializer, OvertimeSerializer, LeavesSerializer, AdjustmentSerializer, BranchSerializer, DepartmentSerializer, DivisionSerializer, RankSerializer, PositionSerializer, ProvinceSerializer, CityMunicipalitySerializer

import secret, datetime, jwt
from .functions import number_of_days_before

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data["username"]
        password = request.data["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            user.failed_login_attempts += 1
            user.save()
            raise AuthenticationFailed("Incorrent password!")
        
        # User and Employee information based on login credentials
        user.last_login = datetime.datetime.now()
        user.save()
        serializer = UserSerializer(user)

        employee = get_object_or_404(Employee, employee_number=serializer.data["employee_number"])
        incoming_birthday = number_of_days_before(employee.birthday)
        incoming_anniversary = number_of_days_before(employee.date_hired)
        serializer1 = EmployeeSerializer(employee)

        # JWT
        payload = {
            "id": user.id,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.now()
        }

        token = jwt.encode(payload=payload, key=secret.JWT_SECRET, algorithm="HS256")

        data = {
            "jwt":token, 
            "user":serializer.data, 
            "employee_details":serializer1.data, 
            "incoming_birthday":incoming_birthday, 
            "incoming_anniversary":incoming_anniversary
            }

        return Response(data, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def new_employee(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EmployeeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response()



@api_view(['GET', 'POST'])
def user_list(request):

    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def employee_list(request):
    if request.method == 'GET':
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EmployeeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])   
def employee_detail(request, employee_number):
    try:
        employee = Employee.objects.get(employee_number=employee_number)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EmployeeSerializer(employee, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        employee.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def audittrail_list(request):
    if request.method == 'GET':
        audittrail = AuditTrail.objects.all()
        serializer = AuditTrailSerializer(audittrail, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AuditTrailSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def audittrail_detail(request, pk):
    try:
        audittrail = AuditTrail.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AuditTrailSerializer(audittrail)
        return JsonResponse(serializer.data)        
    
@api_view(['GET', 'POST'])
def dtr_list(request):
    if request.method == 'GET':
        dtr = DTR.objects.all()
        serializer = DTRSerializer(dtr, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DTRSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def dtr_detail(request, pk):
    try:
        dtr = DTR.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DTRSerializer(dtr)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DTRSerializer(dtr, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        dtr.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def dtrsummary_list(request):
    if request.method == 'GET':
        dtrsummary = DTRSummary.objects.all()
        serializer = DTRSummarySerializer(dtrsummary, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DTRSummarySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def dtrsummary_detail(request, pk):
    try:
        dtrsummary = DTRSummary.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DTRSummarySerializer(dtrsummary)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DTRSummarySerializer(dtrsummary, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        dtrsummary.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def holiday_list(request):
    if request.method == 'GET':
        holiday = Holiday.objects.all()
        serializer = HolidaySerializer(holiday, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HolidaySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def holiday_detail(request, pk):
    try:
        holiday = Holiday.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = HolidaySerializer(holiday)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = HolidaySerializer(holiday, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        holiday.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def obt_list(request):
    if request.method == 'GET':
        obt = OBT.objects.all()
        serializer = OBTSerializer(obt, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OBTSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def obt_detail(request, pk):
    try:
        obt = OBT.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OBTSerializer(obt)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = OBTSerializer(obt, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        obt.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def ot_list(request):
    if request.method == 'GET':
        ot = Overtime.objects.all()
        serializer = OvertimeSerializer(ot, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = OvertimeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ot_detail(request, pk):
    try:
        ot = Overtime.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OvertimeSerializer(ot)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = OvertimeSerializer(ot, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        ot.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def leave_list(request):
    if request.method == 'GET':
        leave = Leaves.objects.all()
        serializer = LeavesSerializer(leave, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LeavesSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def leave_detail(request, pk):
    try:
        leave = Leaves.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LeavesSerializer(leave)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = LeavesSerializer(leave, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        leave.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def adjustment_list(request):
    if request.method == 'GET':
        adjustment = Adjustment.objects.all()
        serializer = AdjustmentSerializer(adjustment, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AdjustmentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def adjustment_detail(request, pk):
    try:
        adjustment = Adjustment.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AdjustmentSerializer(adjustment)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AdjustmentSerializer(adjustment, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        adjustment.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)   
    




@api_view(['GET', 'POST'])
def branch_list(request):
    if request.method == 'GET':
        branch = Branch.objects.all()
        serializer = BranchSerializer(branch, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BranchSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def branch_detail(request, pk):
    try:
        branch = Branch.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BranchSerializer(branch)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BranchSerializer(branch, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        branch.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def department_list(request):
    if request.method == 'GET':
        department = Department.objects.all()
        serializer = DepartmentSerializer(department, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DepartmentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def department_detail(request, pk):
    try:
        department = Department.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DepartmentSerializer(department)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DepartmentSerializer(department, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        department.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def division_list(request):
    if request.method == 'GET':
        division = Division.objects.all()
        serializer = DivisionSerializer(division, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DivisionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def division_detail(request, pk):
    try:
        division = Division.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DivisionSerializer(division)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DivisionSerializer(division, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        division.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def rank_list(request):
    if request.method == 'GET':
        rank = Rank.objects.all()
        serializer = RankSerializer(rank, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RankSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def rank_detail(request, pk):
    try:
        rank = Rank.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RankSerializer(rank)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RankSerializer(rank, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        rank.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def position_list(request):
    if request.method == 'GET':
        position = Position.objects.all()
        serializer = PositionSerializer(position, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PositionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def position_detail(request, pk):
    try:
        position = Position.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PositionSerializer(position)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PositionSerializer(position, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        position.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def province_list(request):
    if request.method == 'GET':
        province = Province.objects.all()
        serializer = ProvinceSerializer(province, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def province_detail(request, pk):
    try:
        province = Province.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProvinceSerializer(province)
        return JsonResponse(serializer.data)



@api_view(['GET'])
def citymunicipality_list(request):
    if request.method == 'GET':
        citymunicipality = CityMunicipality.objects.all()
        serializer = CityMunicipalitySerializer(citymunicipality, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def citymunicipality_detail(request, pk):
    try:
        citymunicipality = CityMunicipality.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CityMunicipalitySerializer(citymunicipality)
        return JsonResponse(serializer.data)