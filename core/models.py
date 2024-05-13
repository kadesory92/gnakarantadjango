from django.db import models

from account.models import User
from school.models import School


class Teacher(models.Model):
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
    photo = models.ImageField(blank=True, null=True)
    certificate = models.FileField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class SchoolTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    date_of_commitment = models.DateField()

    def __str__(self):
        return f"{self.teacher.firstname} {self.teacher.lastname} - {self.school.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
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
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    birth_certificate = models.FileField(blank=True, null=True)
    document = models.FileField(blank=True, null=True)
    last_study_class = models.ForeignKey(StudyClass, related_name='last_students', on_delete=models.SET_NULL,
                                         blank=True, null=True)
    study_class = models.ForeignKey(StudyClass, related_name='current_students', on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    job = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    formation = models.CharField(max_length=200)
    address = models.TextField()
    photo = models.ImageField(blank=True, null=True)
    diploma = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Parenting(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    family_bond = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.parent.firstname} {self.parent.lastname} - {self.student.firstname} {self.student.lastname}"


class TypeExam(models.Model):
    designation = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.designation


class Exam(models.Model):
    designation = models.CharField(max_length=200)
    date_exam = models.DateField()
    coefficient = models.IntegerField()
    type_exam = models.ForeignKey(TypeExam, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.designation} - {self.date_exam}"


class TakeExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    present = models.BooleanField()
    mark = models.FloatField()

    def __str__(self):
        return f"{self.student.firstname} {self.student.lastname} - {self.exam.designation}"


class Attendance(models.Model):
    TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    JUSTIFIED_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
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
    courses = models.ManyToManyField(Course)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.year} - {self.school.name}"
