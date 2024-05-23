from django.urls import path
from . import views

urlpatterns = [
    path('manage_service', views.manage_service, name='manage_service'),
    path('create_service/', views.create_service, name='create_service'),
    path('service_list/', views.service_list, name='service_list'),
    path('service_detail/<int:service_id>/', views.service_detail, name='service_detail'),
    path('update_service/<int:service_id>/', views.update_service, name='update_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),

    path('manage_employee', views.manage_employee, name='manage_employee'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('employee_detail/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('service_employees/<int:service_id>/', views.service_employees, name='service_employees'),
    path('employee_service/<int:employee_id>/', views.employee_service, name='employee_service'),
    path('assign_employee_to_service/<int:employee_id>/', views.assign_employee_to_service,
         name='assign_employee_to_service'),
]