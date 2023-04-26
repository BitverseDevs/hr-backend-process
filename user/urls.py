from django.urls import path
from user import views

urlpatterns = [
    path('api/', views.user_list),
    path('api/<int:pk>/', views.user_detail)
]