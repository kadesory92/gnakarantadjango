from django.db import models

from account.models import User
from service.models import Service


class Founder(models.Model):
    objects = None
    GENDER = [
        (0, 'Féminin'),
        (1, 'Masculin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.IntegerField(choices=GENDER)
    phone = models.CharField(max_length=200)
    bio = models.CharField(max_length=200)
    address = models.TextField()
    photo = models.ImageField(upload_to='founders/photos', blank=True, null=True)
    document = models.FileField(upload_to='founders/documents', blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class School(models.Model):
    objects = None
    CATEGORY = [
        (0, 'Enseignement primaire'),
        (1, 'Enseignement Seconaire')
    ]
    TYPE_SCHOOL = [
        ('public', 'Ecole Publique'),
        ('private', 'Ecole Privée')

    ]
    LEVEL = [
        (0, 'Primaire'),
        (1, 'Collège'),
        (2, 'Lycée'),
        (3, 'Ecole Primaire et Collège'),
        (4, 'Collège et lycée'),
        (5, 'Tous les niveaux')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    founder = models.ForeignKey(Founder, on_delete=models.SET_NULL, null=True, blank=True)
    direction = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='direction_of_education')
    ire = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=TYPE_SCHOOL)
    category = models.IntegerField(choices=CATEGORY)
    level = models.IntegerField(choices=LEVEL)
    phone = models.CharField(max_length=200)
    address = models.TextField(max_length=200, blank=True, null=True)
    site_web = models.URLField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='schools/images', blank=True, null=True)

    def __str__(self):
        return self.name


class Local(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    designation = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.designation


class Staff(models.Model):
    DoesNotExist = None
    objects = None
    GENDER = [
        (0, 'Féminin'),
        (1, 'Masculin'),
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

