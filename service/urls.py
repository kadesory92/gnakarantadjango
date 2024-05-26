from django.urls import path
from . import views

urlpatterns = [

    path('admin/manage_service', views.manage_service, name='admin.manage_service'),
    path('admin/create_service/', views.create_service, name='create_service'),
    path('service_list/', views.service_list, name='service_list'),
    path('detail_service/<int:id>/', views.detail_service, name='detail_service'),
    path('service_detail/<int:id>/', views.service_detail, name='service_detail'),
    path('edit_service/<int:id>/', views.edit_service, name='edit_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),

    path('admin/manage_employee', views.manage_employee, name='admin.manage_employee'),
    path('admin/employee_list/', views.employee_list, name='admin.employee_list'),
    path('admin/employee_detail/<int:id>/', views.employee_detail, name='employee_detail'),
    path('admin/edit_employee/<int:id>/', views.edit_employee, name='admin.edit_employee'),
    path('admin/delete_employee/<int:id>/', views.delete_employee, name='admin.delete_employee'),

    path('service_employees/<int:service_id>/', views.service_employees, name='service_employees'),
    path('employee_service/<int:employee_id>/', views.employee_service, name='employee_service'),
    path('assign_employee_to_service/<int:employee_id>/', views.assign_employee_to_service,
         name='assign_employee_to_service'),
]
