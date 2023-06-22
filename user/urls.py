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

    path('birthdays/', BirthdayView.as_view()),
    path('anniversary/', AnniversaryView.as_view()),

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
]

urlpatterns = format_suffix_patterns(urlpatterns)