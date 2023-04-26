from django.urls import path
from user import views

urlpatterns = [
    path('api/users/', views.user_list),
    path('api/user/<int:pk>/', views.user_detail)
]