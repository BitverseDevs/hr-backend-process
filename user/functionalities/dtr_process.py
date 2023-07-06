import csv, io, pandas as pd, math
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import  status

from user.models import *
from user.serializers import *

from datetime import datetime, date, timedelta, time

def new_dtr_logs_upload(tsv_file):
    try:
        stream = io.StringIO(tsv_file.read().decode('utf-8'))
        columns = ['bio_id', 'datetime_bio', 'duty_in', 'duty_out', 'lunch_out', 'lunch_in', 'branch']
        dframe = pd.read_table(stream, header=None, names=columns)
        dframe = dframe.sort_values(['bio_id', 'datetime_bio'])
        dframe['datetime_bio'] = pd.to_datetime(dframe['datetime_bio'])
        dframe['bio_id'] = dframe['bio_id'].astype(int)
        
        morning_shift_entry = dframe[(dframe['datetime_bio'].dt.hour >= 7) & (dframe['datetime_bio'].dt.hour < 16) & (dframe['duty_out'] == 0)]
        morning_shift_entry['date'] = morning_shift_entry['datetime_bio'].dt.date
        morning_shift_exit = dframe[(dframe['datetime_bio'].dt.hour > 8) & (dframe['datetime_bio'].dt.hour < 18) & (dframe['duty_out'] == 1)]
        morning_shift_exit['date'] = morning_shift_exit['datetime_bio'].dt.date
        morning_shift = pd.concat([morning_shift_entry, morning_shift_exit])        
        grouped_morning_df = morning_shift.groupby(['bio_id', 'date']).agg(datetime_bio_min=('datetime_bio', 'min'), datetime_bio_max=('datetime_bio', 'max')).reset_index()
        grouped_morning_df['branch'] = dframe['branch']
        ids_morning = grouped_morning_df['bio_id'].unique()
        exists = []

        for id in ids_morning:
            select_row = grouped_morning_df[grouped_morning_df["bio_id"] == id]
            employee = get_object_or_404(Employee, bio_id=id)

            for i in range(len(select_row)):
                duty_in = select_row.iloc[i]['datetime_bio_min']
                duty_out = select_row.iloc[i]['datetime_bio_max']
                branch = select_row.iloc[i]['branch']
                date = select_row.iloc[i]['date']
                emp_branch = get_object_or_404(Branch, branch_name=branch)
                schedule = get_object_or_404(ScheduleDaily, emp_no=employee.emp_no, business_date=date)

                dtr_entry_checker = DTR.objects.filter(datetime_bio__gte=duty_in, datetime_bio__lte=duty_out, emp_no=employee.emp_no)
                
                if dtr_entry_checker.exists():
                    exists.append(dtr_entry_checker.first())
                    exists.append(dtr_entry_checker.last())
                    continue

                dtr_morning_in = {
                    'emp_no': employee.emp_no,
                    'bio_id': employee.bio_id,
                    'datetime_bio': duty_in,
                    'flag1_in_out': 0,
                    'entry_type': "DIN",
                    'date_uploaded': datetime.now(),
                    'branch_code': emp_branch.pk,
                    'schedule_daily_code': schedule.pk
                }
                
                dtr_morning_out = {
                    'emp_no': employee.emp_no,
                    'bio_id': employee.bio_id,
                    'datetime_bio': duty_out,
                    'flag1_in_out': 1,
                    'entry_type': "DOUT",
                    'date_uploaded': datetime.now(),
                    'branch_code': emp_branch.pk,
                    'schedule_daily_code': schedule.pk
                }

                dtr_in_serializer = DTRSerializer(data=dtr_morning_in)
                dtr_out_serializer = DTRSerializer(data=dtr_morning_out)

                if dtr_in_serializer.is_valid(raise_exception=True):
                    dtr_in_serializer.save()
                else:
                    return Response(dtr_in_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if dtr_out_serializer.is_valid(raise_exception=True):
                    dtr_out_serializer.save()
                else:
                    return Response(dtr_out_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        night_shift_entry = dframe[(dframe['datetime_bio'].dt.hour >= 20) & (dframe['duty_out'] == 0)]
        night_shift_entry['date'] = night_shift_entry['datetime_bio'].dt.date
        night_shift_exit = dframe[(dframe['datetime_bio'].dt.hour <= 7) & (dframe['duty_out'] == 1)]
        night_shift_exit['date'] = night_shift_exit['datetime_bio'].dt.date - pd.DateOffset(days=1)
        night_shift = pd.concat([night_shift_entry, night_shift_exit])
        night_shift['date'] = pd.to_datetime(night_shift['date']).dt.date
        grouped_night_df = night_shift.groupby(['bio_id', 'date']).agg(datetime_bio_min=('datetime_bio', 'min'), datetime_bio_max=('datetime_bio', 'max')).reset_index()
        grouped_night_df['branch'] = dframe['branch']
        ids_night = grouped_morning_df['bio_id'].unique()
        
        for id in ids_night:
            select_row = grouped_night_df[grouped_night_df['bio_id'] == id]
            employee = get_object_or_404(Employee, bio_id=id)

            for i in range(len(select_row)):
                duty_in = select_row.iloc[i]['datetime_bio_min']
                duty_out = select_row.iloc[i]['datetime_bio_max']
                branch = select_row.iloc[i]['branch']
                date = select_row.iloc[i]['date']
                emp_branch = get_object_or_404(Branch, branch_name=branch)
                schedule = get_object_or_404(ScheduleDaily, emp_no=employee.emp_no, business_date=date)

                dtr_entry_checker = DTR.objects.filter(datetime_bio__gte=duty_in, datetime_bio__lte=duty_out, emp_no=employee.emp_no)

                if dtr_entry_checker.exists():
                    exists.append(dtr_entry_checker.first())
                    exists.append(dtr_entry_checker.last())
                    continue

                dtr_night_in = {
                    'emp_no': employee.emp_no,
                    'bio_id': employee.bio_id,
                    'datetime_bio': duty_in,
                    'flag1_in_out': 0,
                    'entry_type': "DIN",
                    'date_uploaded': datetime.now(),
                    'branch_code': emp_branch.pk,
                    'schedule_daily_code': schedule.pk
                }
                
                dtr_night_out = {
                    'emp_no': employee.emp_no,
                    'bio_id': employee.bio_id,
                    'datetime_bio': duty_out,
                    'flag1_in_out': 1,
                    'entry_type': "DOUT",
                    'date_uploaded': datetime.now(),
                    'branch_code': emp_branch.pk,
                    'schedule_daily_code': schedule.pk
                }

                dtr_in_serializer = DTRSerializer(data=dtr_night_in)
                dtr_out_serializer = DTRSerializer(data=dtr_night_out)

                if dtr_in_serializer.is_valid(raise_exception=True):
                    dtr_in_serializer.save()
                else:
                    return Response(dtr_in_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if dtr_out_serializer.is_valid(raise_exception=True):
                    dtr_out_serializer.save()
                else:
                    return Response(dtr_out_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if exists:
            exist_serializer = DTRSerializer(exists, many=True)
            return Response({"Message": "Successfully uploaded to DTR database. There are existing logs that was uploaded", "Existing Logs": exist_serializer.data}, status=status.HTTP_200_OK)
        return Response({"Message": "Successfully uploaded to DTR database"}, status=status.HTTP_200_OK)           

    except Exception as e:
        return Response({"Error Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def dtr_logs_upload(tsv_file):
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
            exists = []

            for i in range(len(select_row)):
                duty_in = select_row.iloc[i]['datetime_bio_min']
                duty_out = select_row.iloc[i]['datetime_bio_max']
                branch = select_row.iloc[i]['branch']
                date = select_row.iloc[i]['date']
                emp_branch = Branch.objects.get(branch_name=branch)                        
                schedule = ScheduleDaily.objects.get(emp_no=employee.emp_no, business_date=date)

                dtr_entry_checker = DTR.objects.filter(datetime_bio__gte=duty_in, datetime_bio__lte=duty_out, emp_no=employee.emp_no)

                if dtr_entry_checker.exists():
                    exists.append(dtr_entry_checker.first())
                    continue

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
        if exists:
            serializer = DTRSerializer(exists, many=True)
            return Response({"Message": "Successfully uploaded to DTR database. There are existing logs that was uploaded", "Existing logs": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "Successfully uploaded to DTR database"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"Overall error": str(e)}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

def new_merge_dtr_entries(employees, cutoff_code, operation):
    print("Initialization of Merge DTR Entries")
    exists = []
    ND_NIGHT_TIME = time(22, 0, 0)
    ND_BMIDNIGHT_TIME = time(11, 59, 59)
    ND_MIDNIGHT_TIME = time(0, 0, 0)
    ND_MORNING_TIME = time(6, 0, 0)
    ADJUSTMENT_TIME = timedelta(minutes=60)
    try:
        for employee in employees:
            cutoff = Cutoff.objects.get(pk=cutoff_code)
            start_date = cutoff.co_date_from
            end_date = cutoff.co_date_to
            delta = timedelta(days=1)
            while start_date < end_date:

                dtr_date_from = datetime(start_date.year, start_date.month, start_date.day)
                dtr_date_to = datetime(start_date.year, start_date.month, start_date.day, 23, 59, 59)
                print(f"dtr_date_from: {dtr_date_from}")
                print(f"dtr_date_to: {dtr_date_to}")
                schedule = ScheduleDaily.objects.filter(emp_no=employee.emp_no, business_date=start_date)

                if schedule.exists():
                    lates, undertime, total_hours, nd_total_hours, ot_total, nd_ot_total, reg_work_hours, nd_work_hours = 0, 0, 0, 0 ,0, 0, 0, 0
                    obt, ua, restday, sp_holiday, reg_holiday, paid_leave, absent = False, False, False, False, False, False, False
                    duty_in, duty_out, curr_duty_in, curr_duty_out = None, None, None, None
                    
                    business_date = schedule.first().business_date
                    shift_name = schedule.first().schedule_shift_code.name
                    sched_timein = schedule.first().schedule_shift_code.time_in
                    sched_timeout = schedule.first().schedule_shift_code.time_out
                    restday = schedule.first().is_restday
                    
                    if sched_timein > sched_timeout:
                        dtr_date_to += timedelta(days=1)

                    curr_nd_night_time = datetime(dtr_date_from.year, dtr_date_from.month, dtr_date_from.day, ND_NIGHT_TIME.hour, ND_NIGHT_TIME.minute, ND_NIGHT_TIME.second)
                    curr_nd_bmidnight_time = datetime(dtr_date_from.year, dtr_date_from.month, dtr_date_from.day, ND_BMIDNIGHT_TIME.hour, ND_BMIDNIGHT_TIME.minute, ND_BMIDNIGHT_TIME.second)
                    curr_nd_midnight_time = datetime(dtr_date_to.year, dtr_date_to.month, dtr_date_to.day, ND_MIDNIGHT_TIME.hour, ND_MIDNIGHT_TIME.minute, ND_MIDNIGHT_TIME.second)
                    curr_nd_morning_time = datetime(dtr_date_to.year, dtr_date_to.month, dtr_date_to.day, ND_MORNING_TIME.hour, ND_MORNING_TIME.minute, ND_MORNING_TIME.second)

                    curr_sched_timein = datetime(dtr_date_from.year, dtr_date_from.month, dtr_date_from.day, sched_timein.hour, sched_timein.minute, sched_timein.second)
                    curr_sched_timeout = datetime(dtr_date_to.year, dtr_date_to.month, dtr_date_to.day, sched_timeout.hour, sched_timeout.minute, sched_timeout.second)                    
                    
                    dtr_duty_in = DTR.objects.filter(emp_no=employee.emp_no, entry_type="DIN", datetime_bio__gte=dtr_date_from, datetime_bio__lte=curr_sched_timeout)
                    dtr_duty_out = DTR.objects.filter(emp_no=employee.emp_no, entry_type="DOUT", datetime_bio__gte=curr_sched_timein, datetime_bio__lte=dtr_date_to)
                    
                    if dtr_duty_in.exists() and dtr_duty_out.exists():

                        duty_in = dtr_duty_in.first().datetime_bio if dtr_duty_in.exists() else None
                        duty_out = dtr_duty_out.first().datetime_bio if dtr_duty_out.exists() else None

                        if curr_sched_timein < duty_in or duty_out < curr_sched_timeout:
                            obts = OBT.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, obt_date_from__gte=curr_sched_timein, obt_date_to__lte=curr_sched_timeout, obt_approval_status="APD")
                            if obts.exists():
                                obt = True
                                if obts.count() == 1:
                                    if obts.first().obt_date_from <= duty_in:
                                        duty_in = obts.first().obt_date_from
                                    if obts.first().obt_date_to >= duty_out:
                                        duty_out = obts.first().obt_date_to

                                elif obts.count() == 2:
                                    if obts.first().obt_date_from <= duty_in:
                                        duty_in = obts.first().obt_date_from
                                    elif obts.last().obt_date_from <= duty_in:
                                        duty_in = obts.last().obt_date_from

                                    if obts.first().obt_date_to >= duty_out:
                                        duty_out = obts.first().obt_date_to
                                    elif obts.last().obt_date_to >= duty_out:
                                        duty_out = obts.last().obt_date_to       

                            uas = UnaccountedAttendance.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, ua_date_from__gte=curr_sched_timein, ua_date_to__lte=curr_sched_timeout, ua_approval_status="APD")
                            if uas.exists():
                                ua = True
                                if uas.count() == 1:
                                    if uas.first().ua_date_from <= duty_in:
                                        duty_in = uas.first().ua_date_from
                                    if uas.first().ua_date_to >= duty_out:
                                        duty_out = uas.first().ua_date_to

                                elif uas.count() == 2:
                                    if uas.first().ua_date_from <= duty_in:
                                        duty_in = uas.first().ua_date_from
                                    elif uas.last().ua_date_from <= duty_in:
                                        duty_in = uas.last().ua_date_from

                                    if uas.first().ua_date_to >= duty_out:
                                        duty_out = uas.first().ua_date_to
                                    elif uas.last().ua_date_to >= duty_out:
                                        duty_out = uas.last().ua_date_to


                        curr_duty_in = curr_sched_timein if curr_sched_timein > duty_in else duty_in
                        curr_duty_out = curr_sched_timeout if curr_sched_timeout < duty_out else duty_out

                        timein_difference = curr_duty_in - curr_sched_timein
                        if timein_difference > timedelta(minutes=0):
                            lates = math.floor(int(timein_difference.seconds/60))

                        timeout_difference = curr_sched_timeout - curr_duty_out
                        if timeout_difference > timedelta(minutes=0):
                            undertime = math.floor(int(timeout_difference.seconds/60))

                        if sched_timeout > ND_NIGHT_TIME:
                            reg_work_hours = curr_nd_night_time - curr_duty_in
                            nd_work_hours = curr_duty_out - curr_nd_night_time
                            print(reg_work_hours)
                            print(nd_work_hours)
                        elif sched_timein == ND_NIGHT_TIME and ND_MORNING_TIME == sched_timeout:
                            nd_work_hours = (curr_nd_bmidnight_time - curr_duty_in) + (curr_duty_out - curr_nd_midnight_time)
                            print(nd_work_hours)                            

                        else:
                            work_hours = duty_out - duty_in - ADJUSTMENT_TIME                            
                            total_hours = 480 if work_hours >= timedelta(hours=8) else int(work_hours.seconds/60)
                               
                    
                    

                    print(f"curr_sched_timeout: {curr_sched_timeout}")
                    print(f"curr_sched_timein: {curr_sched_timein}")
                    print("")
                    print(f"Employee Number: {employee.emp_no}")
                    print(f"Cutoff Code: {cutoff_code}")
                    print(f"Shift Name: {shift_name}")
                    print(f"Business Date: {business_date}")
                    print(f"Sched Timein: {sched_timein}")
                    print(f"Sched Timeout: {sched_timeout}")
                    print(f"Duty In: {duty_in}")
                    print(f"Duty Out: {duty_out}")
                    print(f"Current Duty In: {curr_duty_in}")                
                    print(f"Current Duty Out: {curr_duty_out}")                

                    print(f"OBT: {obt}")
                    print(f"Unaccounted Attendance: {ua}")

                    print(f"Lates: {lates}")
                    print(f"Undertime: {undertime}")
                    print(f"Total Hours: {total_hours}")
                    print(f"ND Total Hours: {nd_total_hours}")
                    print(f"OT Total: {ot_total}")
                    print(f"ND OT Total: {nd_ot_total}")

                    print(f"Rest Day: {restday}")
                    print(f"SP Holiday: {sp_holiday}")
                    print(f"Reg Holiday: {reg_holiday}")
                    print(f"Paid Leave: {paid_leave}")
                    print(f"Absent: {absent}")
                    
                    

                    print("\n")
                else:
                    return Response({"Schedule Error": f"No Schedule found on employee {employee.emp_no} at business date {start_date.date()}."})

                # break
                start_date += delta
        return Response({"Message": "Sample"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Exception Message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def merge_dtr_entries(employees, cutoff_code, operation):
    exists = []
    try:
        for employee in employees:
            cutoff = Cutoff.objects.get(pk=cutoff_code)
            start_date = cutoff.co_date_from
            end_date = cutoff.co_date_to
            delta = timedelta(days=1)
            while start_date <= end_date:
                dtr_date_from = datetime(start_date.year, start_date.month,start_date.day)
                dtr_date_to = datetime(start_date.year, start_date.month, start_date.day, 23, 59, 59)                
                dtr_entries = DTR.objects.filter(emp_no=employee.emp_no, datetime_bio__gte=dtr_date_from, datetime_bio__lte=dtr_date_to, is_processed=False)
                dtr_entries_processed = DTR.objects.filter(emp_no=employee.emp_no, datetime_bio__gte=dtr_date_from, datetime_bio__lte=dtr_date_to, is_processed=True)
                dtr_summmary = DTRSummary.objects.filter(emp_no=employee.emp_no, business_date=start_date)

                if dtr_summmary.exists():
                    exists.append(dtr_summmary.first())
                    start_date += delta
                    continue

                if dtr_entries.exists() and not dtr_entries_processed and not dtr_summmary.exists():
                    # Initialization of variables
                    business_date = dtr_entries.first().schedule_daily_code.business_date
                    shift_name = dtr_entries.first().schedule_daily_code.schedule_shift_code.name
                    duty_in = dtr_entries.first().datetime_bio
                    duty_out = dtr_entries.last().datetime_bio
                    sched_timein = dtr_entries.first().schedule_daily_code.schedule_shift_code.time_in
                    sched_timeout = dtr_entries.first().schedule_daily_code.schedule_shift_code.time_out
                    curr_sched_timein = datetime(duty_in.year, duty_in.month, duty_in.day, sched_timein.hour, sched_timein.minute, sched_timein.second)                        
                    curr_sched_timeout = datetime(duty_out.year, duty_out.month, duty_out.day, sched_timeout.hour, sched_timeout.minute, sched_timeout.second)
                    late = 0
                    undertime = 0
                    total_hours = 0
                    reg_ot_total = 0
                    nd_ot_total = 0
                    is_obt = False
                    is_ua = False
                    is_sp_holiday = False
                    is_reg_holiday = False

                    # Validation if the employee is late or undertime
                    if curr_sched_timein < duty_in or curr_sched_timeout > duty_out:
                        # On Business Trip
                        obts = OBT.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, obt_approval_status="APD", obt_date_from__gte=dtr_date_from, obt_date_to__lte=dtr_date_to)

                        if obts.exists():
                            is_obt = True

                            if obts.count() == 1:
                                if obts.first().obt_date_from <= duty_in:
                                    duty_in = obts.first().obt_date_from

                                if obts.first().obt_date_to >= duty_out:
                                    duty_out = obts.first().obt_date_to

                            elif obts.count() == 2:
                                if obts.first().obt_date_from <= duty_in:
                                    duty_in = obts.first().obt_date_from

                                elif obts.last().obt_date_from <= duty_in:
                                    duty_in = obts.last().obt_date_from 

                                if obts.first().obt_date_to >= duty_out:
                                    duty_out = obts.first().obt_date_to

                                elif obts.last().obt_date_to >= duty_out:
                                    duty_out = obts.last().obt_date_to

                        #  Unaccounted Attendance
                        uas = UnaccountedAttendance.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, ua_approval_status="APD", ua_date_from__gte=dtr_date_from, ua_date_to__lte=dtr_date_to)

                        if uas.exists():    
                            is_ua = True

                            if uas.count() == 1:
                                if uas.first().ua_date_from <= duty_in:
                                    duty_in = uas.first().ua_date_from

                                if uas.first().ua_date_to >= duty_out:
                                    duty_out = uas.first().ua_date_to

                            elif uas.count() == 2:
                                if uas.first().ua_date_from <= duty_in:
                                    duty_in = uas.first().ua_date_from

                                elif uas.last().ua_date_from <= duty_in:
                                    duty_in = uas.last().ua_date_from

                                if uas.first().ua_date_to >= duty_out:
                                    duty_out = uas.first().ua_date_to

                                elif uas.last().ua_date_to >= duty_out:
                                    duty_out = uas.last().ua_date_to

                    # Overtime
                    ot = Overtime.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, ot_approval_status="APD", ot_date_from__gte=dtr_date_from, ot_date_to__lte=dtr_date_to)

                    if ot.exists():
                        reg_ot_total = ot.first().ot_date_to - ot.first().ot_date_from
                        reg_ot_total = reg_ot_total.seconds/60

                    # Late
                    timein_difference = duty_in - curr_sched_timein

                    if timein_difference > timedelta(minutes=0):
                        late = int(timein_difference.seconds/60)

                    # Undertime 
                    timeout_difference = curr_sched_timeout - duty_out

                    if timeout_difference > timedelta(minutes=0):
                        undertime = int(timeout_difference.seconds/60)

                    # Total work hours
                    work_hours = duty_out - duty_in - timedelta(minutes=60)

                    if work_hours >= timedelta(hours=8):
                        total_hours = 480

                    else:
                        total_hours = int(work_hours.seconds/60)

                    # Holiday
                    holiday = Holiday.objects.filter(holiday_date__gte=dtr_date_from, holiday_date__lte=dtr_date_to)

                    if holiday.exists():
                        if holiday.first().holiday_type == "SH":
                            is_sp_holiday = True

                        elif holiday.first().holiday_type == "LH":
                            is_reg_holiday = True

                    dtr_summary = {
                        "emp_no": employee.emp_no,
                        "cutoff_code": cutoff_code,
                        "business_date": business_date,
                        "shift_name": shift_name,
                        "duty_in": duty_in,
                        "duty_out": duty_out,
                        "sched_timein": sched_timein,
                        "sched_timeout": sched_timeout,
                        "lates": late,
                        "undertime": undertime,
                        "total_hours": total_hours,
                        "reg_ot_total": int(reg_ot_total),
                        "nd_ot_total": nd_ot_total,
                        "is_obt": is_obt,
                        "is_ua": is_ua,
                        "is_reg_holiday": is_reg_holiday,
                        "is_sp_holiday": is_sp_holiday
                    }


                    serializer = DTRSummarySerializer(data=dtr_summary)

                    if serializer.is_valid():
                        # Changing the DTR Entry is_processed to True

                        dtr_entry_in = DTR.objects.get(pk=dtr_entries.first().pk)
                        dtr_entry_in.is_processed = True
                        dtr_entry_in.save()                        

                        dtr_entry_out = DTR.objects.get(pk=dtr_entries.last().pk)
                        dtr_entry_out.is_processed = True
                        dtr_entry_out.save()
                        
                        serializer.save()

                        

                    else:
                        return Response({"Location": "DTR Entry", "Error": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)



                elif not dtr_entries.exists() and not dtr_entries_processed and not dtr_summmary.exists():

                    schedule_daily = ScheduleDaily.objects.filter(emp_no=employee.emp_no, business_date__gte=dtr_date_from, business_date__lte=dtr_date_to)

                    if schedule_daily.exists():
                        business_date = schedule_daily.first().business_date
                        shift_name = schedule_daily.first().schedule_shift_code.name
                        duty_in = None
                        duty_out = None
                        sched_timein = schedule_daily.first().schedule_shift_code.time_in
                        sched_timeout = schedule_daily.first().schedule_shift_code.time_out
                        total_hours = 0
                        paid_leave = False
                        leave_type = None
                        is_obt = False
                        is_ua = False
                        is_sp_holiday = False
                        is_reg_holiday = False
                        is_absent = False

                        # Holiday
                        holiday = Holiday.objects.filter(holiday_date__gte=dtr_date_from, holiday_date__lte=dtr_date_to)                                

                        if holiday.exists():
                            if holiday.first().holiday_type == "SH":
                                is_sp_holiday = True

                            elif holiday.first().holiday_type == "LH":
                                is_reg_holiday = True

                        # Leave Application
                        leaves = Leaves.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, leave_approval_status="APD", leave_date_from__gte=dtr_date_from, leave_date_to__lte=dtr_date_to)                

                        if leaves.exists():
                            leave_type = leaves.first().leave_type.name
                            paid_leave = leaves.first().leave_type.is_paid

                        # On Business Trip
                        obts = OBT.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, obt_approval_status="APD", obt_date_from__gte=dtr_date_from, obt_date_to__lte=dtr_date_to)

                        if obts.exists():
                            is_obt = True
                            duty_in = obts.first().obt_date_from
                            duty_out = obts.first().obt_date_to
                            total_hours = duty_out - duty_in
                            total_hours = int(total_hours.seconds/60)

                        # Unaccounted Attendance
                        uas = UnaccountedAttendance.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, ua_approval_status="APD", ua_date_from__gte=dtr_date_from, ua_date_to__lte=dtr_date_to)
                        if uas.exists():
                            is_ua = True
                            duty_in = uas.first().ua_date_from
                            duty_out = uas.first().ua_date_to
                            total_hours = duty_out - duty_in
                            total_hours = int(total_hours.seconds/60)

                        # Absent                                
                        if is_sp_holiday == False and is_reg_holiday == False and leave_type == None and is_obt == False and is_ua == False:
                            is_absent = True

                        dtr_summary = {
                            "emp_no": employee.emp_no,
                            "cutoff_code": cutoff_code,
                            "business_date": business_date,
                            "shift_name": shift_name,
                            "duty_in": duty_in,
                            "duty_out": duty_out,
                            "sched_timein": sched_timein,
                            "sched_timeout": sched_timeout,
                            "undertime": 0,
                            "lates": 0, 
                            "total_hours": total_hours,
                            "is_paid_leave": paid_leave,
                            "paid_leave_type": leave_type,
                            "reg_ot_total": 0,
                            "nd_ot_total": 0,
                            "is_obt": is_obt,
                            "is_ua": is_ua,
                            "is_sp_holiday": is_sp_holiday,
                            "is_reg_holiday": is_reg_holiday,
                            "is_absent": is_absent,
                        }

                        serializer = DTRSummarySerializer(data=dtr_summary)

                        if serializer.is_valid():
                            serializer.save()

                        else:
                            return Response({"Location": "Schedule Shift", "Error": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



                    elif not schedule_daily.exists() and not dtr_summmary.exists():
                        is_restday = True

                        dtr_summary = {
                            "emp_no": employee.emp_no,
                            "cutoff_code": cutoff_code,
                            "business_date": date(start_date.year, start_date.month, start_date.day),
                            "shift_name": "RD",
                            "duty_in": None,
                            "duty_out": None,
                            "sched_timein": None,
                            "sched_timeout": None,
                            "undertime": 0,
                            "lates": 0,
                            "total_hours": 0,
                            "is_paid_leave": False,
                            "paid_leave_type": None,
                            "reg_ot_total": 0,
                            "nd_ot_total": 0,
                            "is_obt": False,
                            "is_ua": False,
                            "is_sp_holiday": False,
                            "is_reg_holiday": False,
                            "is_absent": False,
                            "is_sched_restday": is_restday
                        }

                        serializer = DTRSummarySerializer(data=dtr_summary)

                        if serializer.is_valid():
                            serializer.save()

                        else:
                            return Response({"Location": "Restday", "Error": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                                            

                start_date += delta                                        


    except Exception as e:
        return Response({"Exception Message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if operation == "list":
        if exists:
            serializer = DTRSummarySerializer(exists, many=True)
            return Response({"Message": "Successfully merge DTR for selected employees but there are employees that have already been merged", "Existing DTR Summary": serializer.data}, status=status.HTTP_200_OK)
        return Response({"Message": "Successfully merge DTR for selected employees"}, status=status.HTTP_200_OK)
    elif operation == "null":
        if exists:
            serializer = DTRSummarySerializer(exists, many=True)
            return Response({"Message": "Successfully merge DTR for selected employees but there are employees that have already been merged", "Existing DTR Summary": serializer.data}, status=status.HTTP_200_OK)
        return Response({"Message": "Successfully merge DTR for all employees with the same payroll group code"}, status=status.HTTP_200_OK)    

def create_dtr_cutoff_summary(employees, cutoff_code, cutoff_start_date, cutoff_end_date, operation):
    exists = []
    try:
        for employee in employees:
            # dtr_summaries = DTRSummary.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, business_date__gte=cutoff_start_date, business_date__lte=cutoff_end_date)
            dtr_summaries = DTRSummary.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, business_date__gte=cutoff_start_date, business_date__lte=cutoff_end_date, is_computed=False)
            dtr_summaries_checker = DTRSummary.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code, business_date__gte=cutoff_start_date, business_date__lte=cutoff_end_date, is_computed=True)
            dtr_cutoff_checker = DTRCutoff.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff_code)

            cutoff_total_hours = 0
            cutoff_lates = 0
            cutoff_undertime = 0
            cutoff_paid_leaves_total = 0
            cutoff_leave_types_used = "."
            leave_types_used_list = []
            cutoff_reg_ot_total = 0
            cutoff_nd_ot_total = 0
            cutoff_sp_holiday_total = 0
            cutoff_sp_holiday_total_hours = 0
            cutoff_reg_holiday_total = 0
            cutoff_absent_total = 0
            hours = 0
            if dtr_cutoff_checker.exists():
                exists.append(dtr_cutoff_checker.first())

            if dtr_summaries.exists() and not dtr_summaries_checker:
                for dtr_summary in dtr_summaries:
                    hours = dtr_summary.total_hours
                    if dtr_summary.is_sp_holiday:
                        hours = 0
                        cutoff_sp_holiday_total_hours += dtr_summary.total_hours
                    cutoff_total_hours += hours
                    cutoff_lates += dtr_summary.lates
                    cutoff_undertime += dtr_summary.undertime
                    cutoff_paid_leaves_total += int(dtr_summary.is_paid_leave)                            
                    cutoff_reg_ot_total += dtr_summary.reg_ot_total
                    cutoff_nd_ot_total += dtr_summary.nd_ot_total
                    cutoff_sp_holiday_total += int(dtr_summary.is_sp_holiday)                    
                    cutoff_reg_holiday_total += int(dtr_summary.is_reg_holiday)
                    cutoff_absent_total += int(dtr_summary.is_absent)

                    if dtr_summary.paid_leave_type:
                        leave_types_used_list.append(dtr_summary.paid_leave_type)



                    if leave_types_used_list:                            
                        cutoff_leave_types_used = cutoff_leave_types_used.join(leave_types_used_list)                            
                    else:
                        cutoff_leave_types_used = None   

                    # Changing the DTR Summary is_computed to True
                    dtr_summary.is_computed = True
                    dtr_summary.save()                         

            if dtr_summaries.exists() and not dtr_summaries_checker:
                dtr_cutoff_summary = {
                    "emp_no": employee.emp_no,
                    "cutoff_code": cutoff_code,
                    "business_date_from": cutoff_start_date.date(),
                    "business_date_to": cutoff_end_date.date(),
                    "total_hours": cutoff_total_hours,
                    "lates_total": cutoff_lates,
                    "undertime_total": cutoff_undertime,
                    "paid_leaves_total": cutoff_paid_leaves_total,
                    "leaves_type_used": cutoff_leave_types_used,
                    "reg_ot_total": cutoff_reg_ot_total,
                    "nd_ot_total": cutoff_nd_ot_total,
                    "sp_holiday_total": cutoff_sp_holiday_total,
                    "sp_holiday_total_hours": cutoff_sp_holiday_total_hours,
                    "reg_holiday_total": cutoff_reg_holiday_total,
                    "absent_total": cutoff_absent_total
                }

                serializer = DTRCutoffSerializer(data=dtr_cutoff_summary)

                if serializer.is_valid():               
                    serializer.save()

                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                            

    except Exception as e:
        return Response({"Error Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    if operation == "list":
        if exists:
            serializer = DTRCutoffSerializer(exists, many=True)
            return Response({"Message": "Successfully created DTR Cutoff Summary for selected employees but there are repetition of entries", "DTR Cutoff Summary": serializer.data}, status=status.HTTP_200_OK)
        return Response({"Message": "Successfully created DTR Cutoff Summary for selected employees"}, status=status.HTTP_200_OK)
    elif operation == "null":
        if exists:
            serializer = DTRCutoffSerializer(exists, many=True)
            return Response({"Message": "Successfully created DTR Cutoff Summary for all employees with the same payroll group code but there are repetition of entries", "DTR Cutoff Summary": serializer.data}, status=status.HTTP_200_OK)
        return Response({"Message": "Successfully created DTR Cutoff Summary for all employees with the same payroll group code"}, status=status.HTTP_200_OK)