from django.db import models

from account.models import User


class Service(models.Model):
    REGION = [
        ('national', 'National'),
        ('boke', 'Boké'),
        ('conakry', 'Conakry'),
        ('faranah', 'Faranah'),
        ('kankan', 'Kankan'),
        ('kindia', 'Kindia'),
        ('labé', 'Labé'),
        ('mamou', 'Mamou'),
        ("nzerekore", "N'Zérékoré")
    ]

    TYPE_SERVICE = [
        ('ministerial_cabinet', 'Cabinet Ministériel'),
        ('national_directorate', 'Direction Nationale'),
        ('ire', 'Inspection Régionale'),
        ('dpe', 'Direction Préfectorale de l\'Education'),
        ('dce', 'Direction Communale de l\'Education'),

    ]
    objects = None
    name = models.CharField(max_length=200)
    type_service = models.CharField(max_length=200, choices=TYPE_SERVICE)
    region = models.CharField(max_length=200, choices=REGION)
    commune = models.CharField(max_length=200, blank=True, null=True)
    prefecture = models.CharField(max_length=200, blank=True, null=True)
    sous_prefecture = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    DoesNotExist = None
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    GENDER = [
        (0, 'Male'),
        (1, 'Female')
    ]
    gender = models.IntegerField(choices=GENDER)
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=100)
    STATUS_CHOICES = (
        ('holder', 'Titulaire'),
        ('contractual', 'Contractuel'),
        ('intern', 'Stagiaire')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    formation = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='employee/photos', blank=True, null=True)
    certificate = models.FileField(upload_to='employee/certificates', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lastname} {self.firstname}"


