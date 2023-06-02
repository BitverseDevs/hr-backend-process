from django.urls import path
from user import views
from .views import UserView, LoginView, EmployeesView, BirthdayView, AnniversaryView, EmployeeUploadView, ExportEmployeeView, DTRView, UploadDTREntryView, CutoffPeriodListView, MergeDTRSummaryView, CreateDTRCutoffSummaryView

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('user/', UserView.as_view()),
    path('login/', LoginView.as_view()),
    path('employees/', EmployeesView.as_view()),
    path('employees/<int:emp_no>/', EmployeesView.as_view()),
    path('birthdays/', BirthdayView.as_view()),
    path('anniversary/', AnniversaryView.as_view()),
    path('import_employee/', EmployeeUploadView.as_view()),
    path('export_employee/', ExportEmployeeView.as_view()),
    path('dtr/<int:pk>/', DTRView.as_view()),
    path('upload_dtr_logs/', UploadDTREntryView.as_view()),
    path('cutoff_period/', CutoffPeriodListView.as_view()),
    path('cutoff_period/<int:pk>/', CutoffPeriodListView.as_view()),
    path('mergedtr/', MergeDTRSummaryView.as_view()),
    path('create_summary/', CreateDTRCutoffSummaryView.as_view()),

    path('test_api/', views.test_view),
    path('test_api/<int:pk>', views.test_view)
]

urlpatterns = format_suffix_patterns(urlpatterns)