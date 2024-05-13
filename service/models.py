from django.db import models

from account.models import User


# class Service(models.Model):
#     objects = None
#     name = models.CharField(max_length=100)
#     type_service = models.CharField(max_length=100)
#     region = models.CharField(max_length=100)
#     commune = models.CharField(max_length=100, blank=True, null=True)
#     prefecture = models.CharField(max_length=100, blank=True, null=True)
#     sous_prefecture = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    type_service = models.CharField(max_length=100)
    region = models.CharField(max_length=100, choices=(
        ('national', 'National'),
        ('Boké', 'Boké'),
        ('Conakry', 'Conakry'),
        ('Faranah', 'Faranah'),
        ('Kankan', 'Kankan'),
        ('Kindia', 'Kindia'),
        ('Labé', 'Labé'),
        ('Mamou', 'Mamou'),
        ("N'Zérékoré", "N'Zérékoré")
    ))
    commune = models.CharField(max_length=100, blank=True, null=True)
    prefecture = models.CharField(max_length=100, blank=True, null=True)
    sous_prefecture = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=100)
    STATUS_CHOICES = (
        ('holder', 'Holder'),
        ('contractual', 'Contractual'),
        ('intern', 'Intern')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    formation = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='employee_photos', blank=True, null=True)
    certificate = models.FileField(upload_to='employee_certificates', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lastname} {self.firstname}"


