from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework import  status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from user.models import User, Employee, AuditTrail, DTR, DTRSummary, Holiday, OBT, Province, CityMunicipality, Overtime, Leaves 
from user.serializers import UserSerializer, EmployeeSerializer, AuditTrailSerializer, DTRSerializer, DTRSummarySerializer, HolidaySerializer, OBTSerializer, ProvinceSerializer, CityMunicipalitySerializer, OvertimeSerializer, LeavesSerializer

import secret
import jwt, datetime

# Start Token with Login and User View

class LoginView(APIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        response = Response()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found!")
        
        if not user.check_password(password):
            user.failed_login_attempts += 1
            user.save()
            raise AuthenticationFailed("Incorrect password!")
        
        # JWT
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }

        user.last_login = datetime.datetime.now()
        user.save()
        serializer = UserSerializer(user)

        employee = get_object_or_404(Employee, employee_number=serializer.data["employee_number"])
        serializer1 = EmployeeSerializer(employee)

        token = jwt.encode(payload, key=secret.JWT_SECRET, algorithm="HS256")
        # response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token,
            "user": serializer.data,
            "employee_details": serializer1.data
        }

        return response
    
class UserView(APIView):
    
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!!!")
        
        try:
            payload = jwt.decode(token, secret.JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")
        
        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)


        return Response(serializer.data)

# End Token with Login and User View

# @csrf_exempt
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