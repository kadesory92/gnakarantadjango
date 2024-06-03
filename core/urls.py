from django.urls import path

from core import views, views_student, views_teacher

urlpatterns = [
    path('', views.home, name='home'),

    path('school/admin/dashboard', views.school_dashboard, name='school_dashboard'),

    path('school/student/manage_student', views_student.manage_student, 'manage_student'),
    path('school/student/create_student', views_student.create_student, name='create_student'),
    path('school/student/detail_student/<int:id>', views_student.detail_student, name='detail_student'),
    path('school/student/edit_student/<int:id>', views_student.edit_student, name='edit_student'),
    path('school/student/delete_student/<int:id>', views_student.delete_student, name='delete_student'),
    path('school/student/enrollment', views_student.enroll_student, name='enrollment_student'),

    path('school/teacher/manage_teacher_by_school', views_teacher.manage_teacher_by_school, 'manage_teacher'),
    path('service/teacher/create_teacher', views_teacher.register_teacher, name='create_teacher'),
    path('service/teacher/assign_subjects/<int:teacher_id>', views_teacher.assign_subjects, name='assign_subjects'),
    path('school/teacher/detail_teacher/<int:id>', views_teacher.detail_teacher, name='detail_teacher'),
    path('school/teacher/edit_teacher/<int:id>', views_teacher.edit_teacher, name='edit_teacher'),
    path('school/teacher/delete_teacher/<int:id>', views_teacher.delete_teacher, name='delete_teacher'),

    path('study_classes/', views.manage_studyClass, name='manage_class'),
    path('study_classes/create/', views.create_studyClass, name='create_class'),
    path('study_classes/<int:class_id>/', views.detail_studyClass, name='detail_class'),
    path('study_classes/<int:class_id>/edit/', views.edit_studyClass, name='edit_class'),
    path('study_classes/<int:class_id>/delete/', views.delete_studyClass, name='delete_class'),

    path('school/classrooms/manage_classroom', views.manage_classroom, name='manage_classroom'),
    path('school/classrooms/create/', views.create_classroom, name='create_classroom'),
    path('school/classrooms/detail_classroom/<int:classroom_id>/', views.detail_classroom, name='detail_classroom'),
    path('school/classrooms/edit_classroom/<int:classroom_id>/edit/', views.edit_classroom, name='edit_classroom'),
    path('school/classrooms/delete_classroom/<int:classroom_id>/delete/', views.delete_classroom,
         name='delete_classroom'),
]
