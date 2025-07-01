from django.db import models

from account.models import User
from school.models import School
from service.models import Service


class Teacher(models.Model):
    objects = None
    GENDER = [
        (0, 'Féminin'),
        (1, 'Masculin'),
    ]

    STATUS_TEACHER = [
        (0, 'Fonctionnaire'),
        (1, 'Privé')
    ]

    # LEVEL_OF_STUDY = [
    #     (0, 'CEPE'),
    #     (1, 'BEPC'),
    #     (2, 'BAPEEL'),
    #     (3, 'BACCALAUREAT'),
    #     (4, 'LICENCE'),
    #     (5, 'MASTER'),
    #     (6, 'DOCTORAT')
    # ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    direction = models.ForeignKey(Service, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.IntegerField(choices=GENDER)
    phone = models.CharField(max_length=20)
    status = models.IntegerField(choices=STATUS_TEACHER)
    # study_level = models.CharField(max_length=100, choices=LEVEL_OF_STUDY)
    diploma = models.FileField(upload_to='teachers/documents', blank=True, null=True)
    address = models.TextField(max_length=200)
    photo = models.ImageField(upload_to='teachers/photos', blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class SchoolTeacher(models.Model):
    objects = None
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    date_of_commitment = models.DateField()

    def __str__(self):
        return f"{self.teacher.lastname} {self.teacher.firstname} - {self.school.name}"


class Subject(models.Model):
    objects = None
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Teaching(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_hours = models.IntegerField()

    def __str__(self):
        return f"{self.teacher.firstname} {self.teacher.lastname} - {self.subject.name}"


class StudyClass(models.Model):
    objects = None
    OPTION = [
        (0, 'Enseignement général'),
        (1, 'Sciences Mathématiques'),
        (2, 'Sciences Expérimentales'),
        (3, 'Science Sociale')
    ]

    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    option = models.IntegerField(choices=OPTION)

    def __str__(self):
        return self.designation


class Classroom(models.Model):
    objects = None
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    objects = None
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    date_course = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    study_class = models.ForeignKey(StudyClass, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    coefficient = models.IntegerField()

    def __str__(self):
        return f"{self.subject.name} - {self.date_course}"


class Student(models.Model):
    DoesNotExist = None
    objects = None
    GENDER = [
        (0, 'Féminin'),
        (1, 'Masculin'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER)
    phone = models.CharField(max_length=200)
    birth_certificate = models.FileField(blank=True, null=True)
    document = models.FileField(upload_to='students/documents', blank=True, null=True)
    photo = models.ImageField(upload_to='students/photo', blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Enrollment(models.Model):
    objects = None
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    school = models.ForeignKey(School, related_name='current_school', on_delete=models.CASCADE)
    last_school = models.ForeignKey(School, related_name='last_school', on_delete=models.SET_NULL,
                                    blank=True, null=True)
    last_study_class = models.ForeignKey(StudyClass, related_name='last_class',
                                         on_delete=models.SET_NULL, blank=True, null=True)
    study_class = models.ForeignKey(StudyClass, related_name='current_class', on_delete=models.CASCADE)

    date_enrollment = models.DateField()

    def __str__(self):
        return f"{self.student.lastname}  {self.student.firstname} - {self.school.name}"


class Parent(models.Model):
    GENDER = [
        (0, 'Féminin'),
        (1, 'Masculin'),
    ]
    LEVEL_OF_STUDY = [
        (0, 'CEPE'),
        (1, 'BEPC'),
        (2, 'BAPEEL'),
        (3, 'BACCALAUREAT'),
        (4, 'LICENCE'),
        (5, 'MASTER'),
        (6, 'DOCTORAT')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER)
    phone = models.CharField(max_length=200)
    job = models.CharField(max_length=200, null=True)
    position = models.CharField(max_length=200, null=True)
    formation = models.CharField(max_length=200, null=True)
    address = models.TextField(max_length=200)
    photo = models.ImageField(upload_to='parents/photos', blank=True, null=True)
    study_level = models.CharField(max_length=200, choices=LEVEL_OF_STUDY)

    # students = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Parenting(models.Model):
    LINK = [
        ('mother', 'Mère'),
        ('father', 'Père'),
        ('sister', 'Soeur'),
        ('brother', 'Frère'),
        ('aunt', 'Tante'),
        ('uncle', 'Oncle')
    ]

    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    family_bond = models.CharField(max_length=200, choices=LINK)
    tutor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.parent.firstname} {self.parent.lastname} - {self.student.firstname} {self.student.lastname}"


class Exam(models.Model):
    PERIOD_EXAM = [
        ('MONTHLY', 'Mensuel'),
        ('QUARTERLY', 'Trimestriel'),
        ('SEMI_ANNUAL', 'Semestriel'),
        ('ANNUAL', 'Annuel')
    ]
    MONTHS = [
        (1, 'Janvier'),
        (2, 'Février'),
        (3, 'Mars'),
        (4, 'Avril'),
        (5, 'Mai'),
        (6, 'Juin'),
        (7, 'Juillet'),
        (8, 'Aout'),
        (9, 'Septembre'),
        (10, 'Octobre'),
        (11, 'Novembre'),
        (12, 'Décembre'),
    ]
    month = models.CharField(max_length=2, null=True, blank=True, choices=MONTHS)
    designation = models.CharField(max_length=200)
    period = models.CharField(max_length=200, choices=PERIOD_EXAM)
    date_exam = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.designation} - {self.date_exam}"


class StudentExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    coefficient = models.IntegerField()
    grade_coefficient = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.student.lastname} - {self.exam} - {self.grade}'


class StudentResult(models.Model):
    TYPE_RESULT = [
        ('MONTHLY', 'Mensuel'),
        ('QUARTERLY', 'Trimestriel'),
        ('SEMI_ANNUAL', 'Semestriel'),
        ('ANNUAL', 'Annuel')
    ]

    MONTHS = [
        (1, 'Janvier'),
        (2, 'Février'),
        (3, 'Mars'),
        (4, 'Avril'),
        (5, 'Mai'),
        (6, 'Juin'),
        (7, 'Juillet'),
        (8, 'Aout'),
        (9, 'Septembre'),
        (10, 'Octobre'),
        (11, 'Novembre'),
        (12, 'Décembre'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type_result = models.CharField(max_length=200, choices=TYPE_RESULT)
    month = models.CharField(max_length=2, null=True, blank=True, choices=MONTHS)
    average_monthly = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    average_quarterly = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    average_semi_annual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    average_annual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    year = models.DateField()


class Attendance(models.Model):
    objects = None
    TYPE_CHOICES = [
        ('student', 'Elève'),
        ('teacher', 'Professeur'),
    ]
    ATTENDANCE_STATUS = [
        (0, 'Présent'),
        (1, 'Absent'),
    ]
    JUSTIFIED_CHOICES = [
        ('yes', 'Oui'),
        ('no', 'Non'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS)
    date = models.DateField()
    justified = models.CharField(max_length=3, choices=JUSTIFIED_CHOICES)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        if self.student:
            return f"{self.student.firstname} {self.student.lastname} - {self.date}"
        elif self.teacher:
            return f"{self.teacher.firstname} {self.teacher.lastname} - {self.date}"


class Program(models.Model):
    objects = None
    object = None
    LEVEL = [
        ('primary', 'Primaire'),
        ('college', 'Collège'),
        ('lycee', 'Lycée')
    ]
    level = models.CharField(max_length=200, choices=LEVEL)
    year = models.IntegerField()
    description = models.TextField()
    subjects = models.ManyToManyField(Subject)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return f"{self.year} - {self.description}"
