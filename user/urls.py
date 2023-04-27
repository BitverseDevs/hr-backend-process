from django.urls import path
from user import views

urlpatterns = [
    path('users/', views.user_list),
    path('user/<int:pk>/', views.user_detail),
    path('employees/', views.employee_list),
    path('employee/<int:employee_id>', views.employee_detail),
    path('audittrails/', views.audittrail_list),
    path('audittrail/<int:pk>', views.audittrail_detail),
]