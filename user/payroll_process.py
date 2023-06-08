from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import  status

from user.models import *
from user.serializers import *

from datetime import datetime, date, time, timedelta



def create_payroll(employees, cutoff, operation):
    try:
        for employee in employees:            
            dtr_cutoff = get_object_or_404(DTRCutoff, emp_no=employee.emp_no, cutoff_code=cutoff.pk)
            sss = SSS.objects.filter(emp_no=employee.emp_no)
            pagibig = PAGIBIG.objects.filter(emp_no=employee.emp_no)
            philhealth = Philhealth.objects.filter(emp_no=employee.emp_no)
            cash_advance = CashAdvance.objects.filter(emp_no=employee.emp_no)
            tax = Tax.objects.filter(emp_no=employee.emp_no)            

            sss_contribution = 0.00
            sss_cashloan = 0.00
            sss_calloan = 0.00
            pagibig_contribution = 0.00
            pagibig_cloan = 0.00
            pagibig_hloan = 0.00
            philhealth_contribution = 0.00
            cash_advance_amount = 0.00

            fname = employee.first_name.upper()
            mname = employee.middle_name.upper() if employee.middle_name else ""
            lname = employee.last_name.upper()
            suffix = employee.suffix.upper() if employee.suffix else ""

            if mname and suffix:
                cname = f"{fname} {mname} {lname} {suffix}"
            elif mname and not suffix:
                cname = f"{fname} {mname} {lname}"
            elif not mname and suffix:
                cname = f"{fname} {lname} {suffix}"
            else:
                cname = f"{fname} {lname}"

            run_date = datetime.now()
            accnt_no = employee.accnt_no
            salary_basic = employee.emp_salary_basic if employee.emp_salary_basic else 0.00
            salary_allowance = employee.emp_salary_allowance if employee.emp_salary_allowance else 0.00
            salary_other = employee.emp_salary_other if employee.emp_salary_other else 0.00
            salary_type = employee.emp_salary_type.lower()
            work_days_total = dtr_cutoff.total_hours / 480
            
            if salary_type == "monthly":
                daily_salary_basic = salary_basic / (cutoff.reg_days_total * 2)
                daily_salary_allowance = salary_allowance / (cutoff.reg_days_total * 2)
                daily_salary_other = salary_other / (cutoff.reg_days_total * 2)
            else:
                daily_salary_basic = salary_basic
                daily_salary_allowance = salary_allowance
                daily_salary_other = salary_other

            daily_total = daily_salary_basic + daily_salary_allowance + daily_salary_other
            daily_hour = daily_total/8
            daily_minute = daily_hour/60

            leaves_amount = dtr_cutoff.paid_leaves_total * daily_total
            ot_amount = dtr_cutoff.reg_ot_total * (daily_minute*1.1)
            nd_amount = 0.00
            reg_holiday_amount = dtr_cutoff.reg_holiday_total * daily_total
            sp_holiday_amount = dtr_cutoff.sp_holiday_total_hours * (daily_minute * 0.3)

            lates_amount = dtr_cutoff.lates_total * daily_minute
            utime_amount = dtr_cutoff.undertime_total * daily_minute     

            if sss.exists():
                sss_contribution = sss.first().sss_contribution_month / 2 if sss.first().sss_contribution_month else 0.00
                sss_cashloan = sss.first().sss_with_cashloan_amount / 2 if sss.first().sss_with_cashloan_amount else 0.00
                sss_calloan = sss.first().sss_with_calloan_amount / 2 if sss.first().sss_with_calloan_amount else 0.00

            if pagibig.exists():
                pagibig_contribution = pagibig.first().pagibig_contribution_month / 2 if pagibig.first().pagibig_contribution_month else 0.00
                pagibig_cloan = pagibig.first().pagibig_with_cloan_amount / 2 if pagibig.first().pagibig_with_cloan_amount else 0.00
                pagibig_hloan = pagibig.first().pagibig_with_hloan_amount / 2 if pagibig.first().pagibig_with_hloan_amount else 0.00

            if philhealth.exists():
                philhealth_contribution = philhealth.first().ph_contribution_month / 2 if philhealth.first().ph_contribution_month else 0.00  

            if cash_advance.exists():
                cash_advance_amount = cash_advance.first().payment_monthly / 2 if cash_advance.first().payment_monthly else 0.00

            insurance = employee.insurance_life / 2 if employee.insurance_life else 0.00      
            other_deduction = employee.other_deductible / 2 if employee.other_deductible else 0.00

            additions = leaves_amount + ot_amount + nd_amount + reg_holiday_amount + sp_holiday_amount
            deductions = lates_amount + utime_amount + sss_contribution + sss_cashloan + sss_calloan + pagibig_contribution + pagibig_cloan + pagibig_hloan + philhealth_contribution + cash_advance_amount + insurance + other_deduction

            gross_pay = (work_days_total * daily_total) + additions
            tax_amount = 0.00
            net_pay = gross_pay - deductions - tax_amount

            absent_amount = dtr_cutoff.absent_total

            payroll_data = {
                "pr_cutoff_code": cutoff.pk,
                "emp_no": employee.emp_no,
                "emp_cname": cname,
                "run_date": run_date,
                "accnt_no": accnt_no,
                "salary_basic": salary_basic,
                "salary_allowance": salary_allowance,
                "salary_other": salary_other,
                "salary_type": salary_type,
                "work_days_total": int(work_days_total),
                "daily_salary_basic": daily_salary_basic,
                "daily_salary_allowance": daily_salary_allowance,
                "daily_salary_other": daily_salary_other,
                "leaves_amount_a": leaves_amount,
                "ot_amount_a": ot_amount,
                "nd_amount_a": nd_amount,
                "reg_holiday_amount_a": reg_holiday_amount,
                "sp_holiday_amount_a": sp_holiday_amount,
                "lates_amount_d": lates_amount,
                "utime_amount_d": utime_amount,
                "sssc_amount_d": sss_contribution,
                "sss_cashloan_d": sss_cashloan,
                "sss_calloan_d": sss_calloan,
                "pagibigc_amount_d": pagibig_contribution,
                "pagibig_cloan_d": pagibig_cloan,
                "pagibig_hloan_d": pagibig_hloan,
                "philhealthc_amount_d": philhealth_contribution,
                "cash_advance_amount_d": cash_advance_amount,
                "insurance_d": insurance,
                "other_d": other_deduction,
                "gross_pay": gross_pay,
                "tax_amount_d": tax_amount,
                "net_pay": net_pay,
                "absent_amount": absent_amount,
            }

            # print(payroll_data)
            serializer = PayrollSerializer(data=payroll_data)

            if serializer.is_valid():
                # sss, pagibig, cash_advance, tax, dtr_cutoff.is_processed
                
                serializer.save()

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"Message": "Sample message"}, status=status.HTTP_200_OK)
            

    except Exception as e:
        return Response({"Error Message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if operation == "list":
        return Response({"Message": "Successfully created a payroll for the selected employees"}, status=status.HTTP_201_CREATED)

    elif operation == "null":
        return Response({"Message": "Successfully created a payroll for all employees within the same payroll group"}, status=status.HTTP_201_CREATED)
