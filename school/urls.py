from django.urls import path
from . import views

urlpatterns = [
    # path('founder/register', views.create_founder, name='register_founder'),
    path('school/create_school', views.create_school, name='create_school'),
    path('school/list_schools', views.list_schools, name='list_schools'),
    path('school/school_detail/<int:id>/', views.detail_school, name='detail_school')
]
