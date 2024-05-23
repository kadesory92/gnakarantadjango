from django.db import models

from account.models import User
from service.models import Service


class Founder(models.Model):
    GENDER = [
        ('female', 'Féminin'),
        ('male', 'Masculin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=100, choices=GENDER)
    phone = models.CharField(max_length=200)
    bio = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    address = models.TextField()
    photo = models.ImageField(upload_to='founders/photos', blank=True, null=True)
    document = models.FileField(upload_to='founders/documents', blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class School(models.Model):
    TYPE_SCHOOL = [
        ('preschool', 'Préscolaire'),
        ('primary', 'Primaire'),
        ('secondary', 'Secondaire')

    ]
    LEVEL = [
        ('primary', 'Primaire'),
        ('college_cycle', 'Collège'),
        ('high_school_cycle', 'Lycée'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    founder = models.ForeignKey(Founder, on_delete=models.SET_NULL, null=True, blank=True)
    direction = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='direction_of_education')
    ire = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True,
                            related_name='inspection_regional')
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=TYPE_SCHOOL)
    category = models.CharField(max_length=200)
    level = models.CharField(max_length=200, choices=LEVEL)
    phone = models.CharField(max_length=200)
    address_email = models.EmailField(max_length=200, blank=True, null=True)
    site_web = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='schools/images', blank=True, null=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    GENDER = [
        ('female', 'Féminin'),
        ('male', 'Masculin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=200, choices=GENDER)
    phone = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    formation = models.CharField(max_length=200)
    address = models.TextField()
    photo = models.ImageField(upload_to='staffs/images', blank=True, null=True)
    certificate = models.FileField(upload_to='staffs/documents', blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Local(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    designation = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.designation
