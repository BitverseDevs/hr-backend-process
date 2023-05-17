from django.urls import path
from user import views
from .views import UserView, LoginView, EmployeesListView, EmployeesView, BirthdayView, AnniversaryView, TsvFileUploadView, EmployeeUploadView, ExportEmployeeView

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('user/', UserView.as_view()),
    path('login/', LoginView.as_view()),
    path('employees_list/', EmployeesListView.as_view()),
    path('employees/', EmployeesView.as_view()),
    path('employees/<int:employee_number>/', EmployeesView.as_view()),
    path('birthdays/', BirthdayView.as_view()),
    path('anniversary/', AnniversaryView.as_view()),
    path('upload_DTR_logs/', TsvFileUploadView.as_view()),
    path('import_employee/', EmployeeUploadView.as_view()),
    path('export_employee/', ExportEmployeeView.as_view()),

    path('test_api/<int:pk>', views.test_view)
]

urlpatterns = format_suffix_patterns(urlpatterns)