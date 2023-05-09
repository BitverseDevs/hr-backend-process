from django.urls import path
from user import views
from .views import LoginView

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
    path('holidays/', views.holiday_list),
    path('holiday/<int:pk>', views.holiday_detail),
    path('obts/', views.obt_list),
    path('obt/<int:pk>', views.obt_detail),
    path('ots/', views.ot_list),
    path('ot/<int:pk>', views.ot_detail),
    path('leaves/', views.leave_list),
    path('leave/<int:pk>', views.leave_detail),
    path('adjustments/', views.adjustment_list),
    path('adjustment/<int:pk>', views.adjustment_detail),

    path('branches/', views.branch_list),
    path('branch/<int:pk>', views.branch_detail),
    path('departments/', views.department_list),
    path('department/<int:pk>', views.department_detail),
    path('divisions/', views.division_list),
    path('division/<int:pk>', views.division_detail),
    path('ranks/', views.rank_list),
    path('rank/<int:pk>', views.rank_detail),
    path('positions/', views.position_list),
    path('position/<int:pk>', views.position_detail),
    path('provinces/', views.province_list),
    path('province/<int:pk>', views.province_detail),
    path('citiesmunicipalities/', views.citymunicipality_list),
    path('citiesmunicipalities/<int:pk>', views.citymunicipality_detail),

    path('login/', LoginView.as_view()),
]