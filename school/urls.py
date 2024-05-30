from django.urls import path
from . import views

urlpatterns = [
    # path('founder/register', views.create_founder, name='register_founder'),
    path('school/create_school', views.create_school, name='create_school')
]
