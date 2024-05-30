from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('SUPER_ADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('SERVICE_ADMIN', 'Service Admin'),
        ('SERVICE_MANAGER', 'Service Manager'),
        ('FOUNDER', 'Fondateur'),
        ('SERVICE_STAFF', 'Service Staff'),
        ('ADMIN_IRE', 'Admin IRE'),
        ('ADMIN_DPE', 'Admin DPE'),
        ('ADMIN_DCE', 'Admin DCE'),
        ('STAFF_IRE', 'Personnel de IRE'),
        ('STAFF_DCE', 'Personnel de DCE'),
        ('STAFF_DPE', 'Personnel de DPE'),
        ('SCHOOL_ADMIN', 'School Admin'),
        ('SCHOOL_MANAGER', 'School Manager'),
        ('SCHOOL', 'School'),
        ('SCHOOL_STAFF', 'Personnel d\'école'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
        ('PARENT', 'Parent'),
    )
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return self.email


