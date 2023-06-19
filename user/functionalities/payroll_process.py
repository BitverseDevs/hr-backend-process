from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import  status

from user.models import *
from user.serializers import *

from datetime import datetime

import math



def create_payroll(employees, cutoff, operation):
    try:
        for employee in employees:
            dtr_cutoff = DTRCutoff.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff.pk, is_processed=False).first()
            dtr_cutoff_checker = DTRCutoff.objects.filter(emp_no=employee.emp_no, cutoff_code=cutoff.pk, is_processed=True).first()

            if dtr_cutoff_checker:
                return Response({"Message": f"Employee {employee.first_name} {employee.last_name} payroll account has already been processed"})
            
            allowance_entries = AllowanceEntry.objects.filter(emp_no=employee.emp_no)
            sss = SSS.objects.filter(emp_no=employee.emp_no)
            pagibig = PAGIBIG.objects.filter(emp_no=employee.emp_no)
            philhealth = Philhealth.objects.filter(emp_no=employee.emp_no)
            payroll_group = PayrollGroup.objects.get(pk=cutoff.payroll_group_code.pk)           
            tax = Tax.objects.filter(emp_no=employee.emp_no)
            cash_advance = CashAdvance.objects.filter(emp_no=employee.emp_no, is_fully_paid=False)



            salary_allowance = 0.00
            salary_other = 0.00
            daily_salary_other = 0.00
            cash_advance_amount = 0.00



            if employee.middle_name and employee.suffix:
                cname = f"{employee.first_name} {employee.middle_name} {employee.last_name} {employee.suffix}"
            elif employee.middle_name and not employee.suffix:
                cname = f"{employee.first_name} {employee.middle_name} {employee.last_name}"
            elif not employee.middle_name and employee.suffix:
                cname = f"{employee.first_name} {employee.last_name} {employee.suffix}"
            else:
                cname = f"{employee.first_name} {employee.last_name}"

            if allowance_entries.exists():
                for allowance in allowance_entries:
                    salary_allowance += allowance.amount

            annual_reg_working_days = 261

            if employee.emp_salary_type == "monthly":
                daily_salary_basic = (employee.emp_salary_basic * 12) / annual_reg_working_days
                daily_salary_allowance = (salary_allowance * 12) / annual_reg_working_days
                # daily_salary_other = (salary_other * 12) / annual_reg_working_days
            else:
                daily_salary_basic = employee.emp_salary_basic
                daily_salary_allowance = salary_allowance
                # daily_salary_other = salary_other
            
            daily_total = daily_salary_basic + daily_salary_allowance
            daily_total_minute = daily_total/480

            leave_amount = dtr_cutoff.paid_leaves_total * daily_total
            ot_amount = dtr_cutoff.reg_ot_total * ((daily_salary_basic/480) * 1.1)
            nd_amount = 0.00
            reg_holiday_amount = dtr_cutoff.reg_holiday_total * daily_total
            sp_holiday_amount = (dtr_cutoff.sp_holiday_total * daily_total) + (dtr_cutoff.sp_holiday_total_hours * (daily_total_minute * 0.3))
            
            work_days_total = dtr_cutoff.total_hours/480

            # Deduction of lates and undertime is per 30mins
            # if (dtr_cutoff.total_hours % 60) / 60 >= 0.5:
            #     init_work_days_total = (dtr_cutoff.total_hours // 60) + 0.5
            # else:
            #     init_work_days_total = dtr_cutoff.total_hours // 60
        
            # work_days_total = init_work_days_total / 8          

            lates_amount = dtr_cutoff.lates_total * daily_total_minute
            utime_amount = dtr_cutoff.undertime_total * daily_total_minute

            additions = leave_amount + ot_amount + nd_amount + reg_holiday_amount + sp_holiday_amount            
            gross_pay = (work_days_total * daily_total) + additions  + lates_amount + utime_amount

            # Deduction of lates and undertime is per 30mins
            # lates_time_30 = dtr_cutoff.lates_total//30
            # # print(f"dtr_cutoff.lates_total: {dtr_cutoff.lates_total}")
            # # print(f"lates_time: {lates_time_30}")
            # lates_remainder = (dtr_cutoff.lates_total%30)
            # # print(f"lates_remainder: {lates_remainder}")
            # lates_amount = lates_time_30 * (daily_total_minute * 30)
            # # lates_amount = dtr_cutoff.lates_total * daily_total_minute

            # utime_time_30 = math.ceil((dtr_cutoff.undertime_total + lates_remainder)/30)
            # # print(f"dtr_cutoff.undertime_total: {dtr_cutoff.undertime_total}")
            # # print(f"utime_time: {utime_time_30}")
            # utime_amount = utime_time_30 * (daily_total_minute * 30)
            # # utime_amount = dtr_cutoff.undertime_total * daily_total_minute

            # lates_utime_total = math.ceil((dtr_cutoff.lates_total + dtr_cutoff.undertime_total)/30)
            # # print(f"lates and utime: {dtr_cutoff.lates_total + dtr_cutoff.undertime_total}")
            # # print(f"lates_utime_time: {lates_utime_time}")
            # lates_utime_amount = lates_utime_total * (daily_total_minute * 30)
            # # print(f"lates_utime_deduction: {lates_utime_amound}")
            # lates_utime_amount = lates_amount + utime_amount



            if sss.exists():
                sss_contribution = sss.first().sss_contribution_month / 2 if sss.first().sss_contribution_month else 0.00                
                if sss.first().sss_with_cashloan_amount != 0 or sss.first().sss_with_cashloan_amount != None:
                    sss_cashloan = sss.first().sss_with_cashloan_amount / 2 if sss.first().sss_with_cashloan_amount else 0.00
                if sss.first().sss_with_calloan_amount != 0 or sss.first().sss_with_calloan_amount != None:
                    sss_calloan = sss.first().sss_with_calloan_amount / 2 if sss.first().sss_with_calloan_amount else 0.00

            if pagibig.exists():
                pagibig_contribution = pagibig.first().pagibig_contribution_month / 2 if pagibig.first().pagibig_contribution_month else 0.00
                if pagibig.first().pagibig_with_cloan_amount != 0 or pagibig.first().pagibig_with_cloan_amount != None:
                    pagibig_cloan = pagibig.first().pagibig_with_cloan_amount / 2 if pagibig.first().pagibig_with_cloan_amount else 0.00
                if pagibig.first().pagibig_with_hloan_amount != 0 or pagibig.first().pagibig_with_hloan_amount != None:
                    pagibig_hloan = pagibig.first().pagibig_with_hloan_amount / 2 if pagibig.first().pagibig_with_hloan_amount else 0.00

            if philhealth.exists():
                philhealth_contribution = philhealth.first().ph_contribution_month / 2 if philhealth.first().ph_contribution_month else 0.00



            deductions = sss_contribution + pagibig_contribution + philhealth_contribution + lates_amount + utime_amount
            net_before_tax = gross_pay - deductions            

            tax_basic_bracket = TaxBasicBracket.objects.get(frequency=payroll_group.payroll_freq, ramount_from__lte=net_before_tax, ramount_to__gte=net_before_tax)            

            tax_amount = net_before_tax * tax_basic_bracket.amount_rate
            tax_amount += tax_basic_bracket.fix_tax_amount

            net_after_tax = net_before_tax - tax_amount

            if cash_advance.exists():
                if cash_advance.first().cash_advance_remaining != 0:
                    cash_advance_amount = cash_advance.first().payment_monthly / 2 if cash_advance.first().payment_monthly else 0.00                    
            
            insurance_amount = employee.insurance_life / 2 if employee.insurance_life else 0.00
            other_deduction = employee.other_deductible / 2 if employee.other_deductible else 0.00            
            deductions_after_tax = cash_advance_amount + insurance_amount + other_deduction + sss_cashloan + sss_calloan + pagibig_cloan + pagibig_hloan

            net_pay = net_after_tax - deductions_after_tax
            


            payroll = {
                "pr_cutoff_code": cutoff.pk,
                "emp_no" : employee.emp_no,
                "emp_cname": cname,
                "run_date": datetime.now(),
                "accnt_no": employee.accnt_no,
                "salary_basic": employee.emp_salary_basic if employee.emp_salary_basic else 0.00,
                "salary_allowance": salary_allowance,
                "salary_other": salary_other,
                "salary_type": employee.emp_salary_type,
                "daily_salary_basic": daily_salary_basic,
                "daily_salary_allowance": daily_salary_allowance,
                "daily_salary_other": daily_salary_other,
                "leaves_amount_a": leave_amount,
                "ot_amount_a": ot_amount,
                "nd_amount_a": nd_amount,
                "reg_holiday_amount_a": reg_holiday_amount,
                "sp_holiday_amount_a": sp_holiday_amount,
                "work_days_total": work_days_total,
                "gross_pay": gross_pay,
                "lates_amount_d": lates_amount,
                "utime_amount_d": utime_amount,
                "sssc_amount_d": sss_contribution,
                "pagibigc_amount_d": pagibig_contribution,
                "philhealthc_amount_d": philhealth_contribution,
                "tax_amount_d": tax_amount,
                "sss_cashloan_d": sss_cashloan,
                "sss_calloan_d": sss_calloan,
                "pagibig_cloan_d": pagibig_cloan,
                "pagibig_hloan_d": pagibig_hloan,
                "cash_advance_amount_d": cash_advance_amount,
                "insurance_d": insurance_amount,
                "other_d": other_deduction,
                "net_pay": net_pay,
                "absent_amount": dtr_cutoff.absent_total
            }

            # print(payroll)
            serializer = PayrollSerializer(data=payroll)
            if serializer.is_valid():
                dtr_cutoff.is_processed = True
                dtr_cutoff.save()
                
                if sss.exists():
                    sss_instance = sss.first()
                    if sss_instance.sss_rem_cashloan_amount != 0 and sss_instance.sss_rem_cashloan_amount != None:
                        sss_instance.sss_rem_cashloan_amount -= sss_cashloan
                    elif sss_instance.sss_rem_cashloan_amount == 0:
                        sss_instance.sss_with_cashloan_amount = 0

                    if sss_instance.sss_rem_calloan_amount != 0 and sss_instance.sss_rem_calloan_amount != None:
                        sss_instance.sss_rem_calloan_amount -= sss_calloan
                    elif sss_instance.sss_rem_calloan_amount == 0:
                        sss_instance.sss_with_calloan_amount = 0

                    sss_instance.save()

                if pagibig.exists():
                    pagibig_instance = pagibig.first()
                    if pagibig_instance.pagibig_rem_cloan_amount != 0 and pagibig_instance.pagibig_rem_cloan_amount != None:
                        pagibig_instance.pagibig_rem_cloan_amount -= pagibig_cloan
                    elif pagibig_instance.pagibig_rem_cloan_amount == 0:
                        pagibig_instance.pagibig_with_cloan_amount = 0

                    if pagibig_instance.pagibig_rem_hloan_amount != 0 and pagibig_instance.pagibig_rem_hloan_amount != None:
                        pagibig_instance.pagibig_rem_hloan_amount -= pagibig_hloan
                    elif pagibig_instance.pagibig_rem_hloan_amount == 0:
                        pagibig_instance.pagibig_with_hloan_amount = 0

                    pagibig_instance.save()

                if cash_advance.exists():
                    cash_advance_instance = cash_advance.first()
                    if cash_advance_instance.cash_advance_remaining != 0:
                        cash_advance_instance.cash_advance_remaining -= cash_advance_amount
                        cash_advance_instance.last_payment_amount = cash_advance_amount
                        cash_advance_instance.date_last_payment = datetime.now()
                    elif cash_advance_instance.cash_advance_remaining == 0:
                        cash_advance_instance.is_fully_paid = True

                    cash_advance_instance.save()

                serializer.save()
            
            else:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"Error Message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if operation == "list":
        return Response({"Message": "Successfully created a payroll for the selected employees"}, status=status.HTTP_201_CREATED)

    elif operation == "null":
        return Response({"Message": "Successfully created a payroll for all employees within the same payroll group"}, status=status.HTTP_201_CREATED)