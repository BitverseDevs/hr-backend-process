from django.urls import path
from user import views

urlpatterns = [
    path('users/', views.user_list),
    path('user/<int:pk>/', views.user_detail),
    path('employees/', views.employee_list),
    path('employee/<int:employee_number>', views.employee_detail),
    path('audittrails/', views.audittrail_list),
    path('audittrail/<int:pk>', views.audittrail_detail),
    path('dtrs/', views.dtr_list),
    path('dtr/<int:pk>', views.dtr_detail),
    path('dtrsummaries/', views.dtrsummary_list),
    path('dtrsummary/<int:pk>', views.dtrsummary_detail),
    path('citiesmunicipalities/', views.citymunicipality_list),
    path('citiesmunicipalities/<int:pk>', views.citymunicipality_detail),
]