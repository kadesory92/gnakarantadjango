from django.urls import path

from core import views

urlpatterns = [
    path('', views.home, name='home'),

    path('school/admin/dashboard', views.school_dashboard, name='school_dashboard'),

    path('create_student/', views.create_student, name='create_student'),
]
