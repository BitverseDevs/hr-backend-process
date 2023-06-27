from django.urls import path
from user import views
from .views import *



from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('user/<int:pk>', UserView.as_view()),

    path('employees/', EmployeesView.as_view()),
    path('employees/<int:emp_no>/', EmployeesView.as_view()),
    path('import_employee/', EmployeeUploadView.as_view()),

    path('branch/', BranchView.as_view()),
    path('branch/<int:pk>/', BranchView.as_view()),
    path('department/', DepartmentView.as_view()),
    path('department/<int:pk>/', DepartmentView.as_view()),
    path('division/', DivisionView.as_view()),
    path('division/<int:pk>/', DivisionView.as_view()),
    path('payrollgroup/', PayrollGroupView.as_view()),
    path('payrollgroup/<int:pk>/', PayrollGroupView.as_view()),
    path('position/', PositionView.as_view()),
    path('position/<int:pk>/', PositionView.as_view()),
    path('rank/', RankView.as_view()),
    path('rank/<int:pk>/', RankView.as_view()),

    path('birthdays/', BirthdayView.as_view()),
    path('anniversary/', AnniversaryView.as_view()),

    path('holiday/', HolidayView.as_view()),
    path('holiday/<int:pk>/', HolidayView.as_view()),
    path('obt/', OBTView.as_view()),
    path('obt/<int:pk>/', OBTView.as_view()),
    path('ot/', OvertimeView.as_view()),
    path('ot/<int:pk>/', OvertimeView.as_view()),
    path('leave_type/', LeaveTypeView.as_view()),
    path('leave_type/<int:pk>/', LeaveTypeView.as_view()),
    path('leave_credit/', LeaveCreditView.as_view()),
    path('leave_credit/<int:pk>/', LeaveCreditView.as_view()),
    path('leave/', LeaveView.as_view()),
    path('leave/<int:pk>/', LeaveView.as_view()),
    path('ua/', UnaccountedAttendanceView.as_view()),
    path('ua/<int:pk>/', UnaccountedAttendanceView.as_view()),
    path('schedule_shift/', ScheduleShiftView.as_view()),
    path('schedule_shift/<int:pk>/', ScheduleShiftView.as_view()),
    path('schedule_daily/', ScheduleDailyView.as_view()),
    path('schedule_daily/<int:pk>/', ScheduleDailyView.as_view()),

    path('tax/', TaxView.as_view()),
    path('tax/<int:emp_no>/', TaxView.as_view()),
    path('pagibig/', PagibigView.as_view()),
    path('pagibig/<int:emp_no>/', PagibigView.as_view()),
    path('sss/', SssView.as_view()),
    path('sss/<int:emp_no>/', SssView.as_view()),
    path('philhealth/', PhilhealthView.as_view()),
    path('philhealth/<int:emp_no>/', PhilhealthView.as_view()),

    path('dtr/', DTRView.as_view()),
    path('dtr/<int:emp_no>/', DTRView.as_view()),
    path('upload_dtr_logs/', UploadDTREntryView.as_view()),

    path('dtr_summary/', DTRSummaryView.as_view()),
    path('dtr_summary/<int:emp_no>/', DTRSummaryView.as_view()),
    path('cutoff_period/', CutoffPeriodListView.as_view()),
    path('cutoff_period/<int:pk>/', CutoffPeriodListView.as_view()),
    path('mergedtr/', MergeDTRSummaryView.as_view()),    
    
    path('dtr_cutoff_summary/', DTRCutoffSummaryView.as_view()),
    path('dtr_cutoff_summary/<int:emp_no>/', DTRCutoffSummaryView.as_view()),
    path('create_summary/', CreateDTRCutoffSummaryView.as_view()),
    
    path('create_payrolls/', CreatePayrollView.as_view()),
    path('payroll/', PayrollView.as_view()),
    path('payroll/<int:emp_no>/', PayrollView.as_view()),
    path('ca/', CashAdvanceView.as_view()),
    path('ca/<int:pk>/', CashAdvanceView.as_view()),
    path('allowance_type/', AllowanceTypeView.as_view()),
    path('allowance_type/<int:pk>/', AllowanceTypeView.as_view()),
    path('allowance_entry/', AllowanceEntryView.as_view()),
    path('allowance_entry/<int:pk>/', AllowanceEntryView.as_view()),
    path('tax_collected/', TaxColletedView.as_view()),
    path('pay13/', Pay13THView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)