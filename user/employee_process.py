import csv

from rest_framework.response import Response
from rest_framework import  status

from user.models import *
from user.serializers import *

from datetime import datetime, date, timedelta



def upload_csv_file_employee(file):
    existing = []
    non_existing = []
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
            
            branch = {
                "main": "Main",
            }

            city = CityMunicipality.objects.filter(pk=row[23])            
            if city.exists():
                city_code = city.first().pk
            else:
                city_code = None

            department = Department.objects.filter(pk=row[24])
            if department.exists():
                department_code = department.first().pk
            else:
                department_code = None

            division = Division.objects.filter(pk=row[25])
            if division.exists():
                division_code = division.first().pk
            else:
                division_code = None

            payroll_group = PayrollGroup.objects.filter(pk=row[26])
            if payroll_group.exists():
                payroll_group_code = payroll_group.first().pk
            else:
                payroll_group_code = None

            position = Position.objects.filter(pk=row[27])
            if position.exists():
                position_code = position.first().pk
            else:
                position_code = None

            rank = Rank.objects.filter(pk=row[28])
            if rank.exists():
                rank_code = rank.first().pk
            else:
                rank_code = None

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
                "bio_id": row[12],
                "date_hired": row[13],        
                "date_added": datetime.now(), 
                "approver": None if row[14] == "" else row[14],
                "emp_salary_allowance": int(row[15]),
                "emp_salary_basic": float(row[16]),
                "emp_salary_other": float(row[17]),
                "emp_salary_type": row[18],
                "insurance_life": float(row[19]),
                "other_deductible": float(row[20]),
                "accnt_no": row[21],
                # "branch_code": ?,
                "city_code": city_code,
                "department_code": department_code,
                "division_code": division_code,
                "payroll_group_code": payroll_group_code,
                "position_code": position_code,
                "rank_code": rank_code
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