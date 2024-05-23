from django.db import models

from account.models import User
from school.models import School


class Teacher(models.Model):
    GENDER = [
        ('female', 'Féminin'),
        ('male', 'Masculin'),
    ]

    STATUS = [
        ('stat_official', 'Fonctionnaire'),
        ('private', 'Privé')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=200, choices=STATUS)
    form_level = models.CharField(max_length=100)
    certificate = models.FileField(upload_to='teachers/documents', blank=True, null=True)
    address = models.TextField(max_length=200)
    photo = models.ImageField(upload_to='teachers/photos', blank=True, null=True)

    # schools = models.ManyToManyField(School)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


#

class SchoolTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    date_of_commitment = models.DateField()

    def __str__(self):
        return f"{self.teacher.lastname} {self.teacher.firstname} - {self.school.name}"


class Subject(models.Model):
    name = models.CharField(max_length=200)
    coefficient = models.IntegerField()

    def __str__(self):
        return self.name


class Teaching(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_hours = models.IntegerField()

    def __str__(self):
        return f"{self.teacher.firstname} {self.teacher.lastname} - {self.subject.name}"


class StudyClass(models.Model):
    designation = models.CharField(max_length=200)

    def __str__(self):
        return self.designation


class Classroom(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Course(models.Model):
    date_course = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    study_class = models.ForeignKey(StudyClass, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name} - {self.date_course}"


class Student(models.Model):
    GENDER = [
        ('female', 'Féminin'),
        ('male', 'Masculin'),
    ]
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
        ('female', 'Féminin'),
        ('male', 'Masculin'),
    ]
    FORMATION = [
        ('college', 'Collège'),
        ('high_school', 'Lycée')
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
    study_level = models.CharField(max_length=200)

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
    TYPE_EXAM = [
        ('MONTHLY', 'Mensuel'),
        ('QUARTERLY', 'Trimestriel'),
        ('SEMI_ANNUAL', 'Semestriel'),
        ('ANNUAL', 'Annuel')
    ]

    designation = models.CharField(max_length=200)
    type_exam = models.CharField(max_length=200, choices=TYPE_EXAM)
    date_exam = models.DateField()
    coefficient = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # type_exam = models.ForeignKey(TypeExam, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.designation} - {self.date_exam}"


# class TakeExam(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     present = models.BooleanField()
#     mark = models.FloatField()
#
#     def __str__(self):
#         return f"{self.student.firstname} {self.student.lastname} - {self.exam.designation}"


class Attendance(models.Model):
    TYPE_CHOICES = [
        ('student', 'Elève'),
        ('teacher', 'Professeur'),
    ]
    STATUS_CHOICES = [
        ('present', 'Présent'),
        ('absent', 'Absent'),
    ]
    JUSTIFIED_CHOICES = [
        ('yes', 'Oui'),
        ('no', 'Non'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
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
    year = models.IntegerField()
    description = models.TextField()
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.year} - {self.school.name}"
