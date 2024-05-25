from django.urls import path
from . import views

urlpatterns = [
    path('admin/dashboard', views.admin_dashboard, name='admin-dashboard'),

    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register/founder/', views.register_founder, name='register_founder'),
    path('admin/register/employee/', views.register_employee, name='register_employee'),
]
