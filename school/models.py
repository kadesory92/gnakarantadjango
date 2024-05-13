from django.db import models

from account.models import User
from service.models import Service


class Founder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    bio = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    address = models.TextField()
    photo = models.ImageField(upload_to='', blank=True, null=True)
    document = models.FileField(upload_to='', blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class School(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    founder = models.ForeignKey(Founder, on_delete=models.SET_NULL, null=True, blank=True)
    direction = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='direction_of_education')
    ire = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True,
                            related_name='inspection_regional')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    address_email = models.EmailField(blank=True, null=True)
    site_web = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    formation = models.CharField(max_length=100)
    address = models.TextField()
    photo = models.ImageField(upload_to='', blank=True, null=True)
    certificate = models.FileField(upload_to='', blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Local(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.designation
