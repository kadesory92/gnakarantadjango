from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/employee/', views.register_employee, name='register_employee'),
]
