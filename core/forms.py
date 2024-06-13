from django import forms
from .models import Student, Enrollment, Teacher, SchoolTeacher, Subject, Teaching, StudyClass, Classroom, Course, \
    Parent, Parenting, Exam, Attendance, Program, StudentExam


class TeacherForm(forms.ModelForm):
    class Meta:
        exclude = ['user']
        model = Teacher
        fields = ['user', 'direction', 'lastname', 'firstname', 'date_of_birth', 'gender', 'phone', 'status',
                  'form_level', 'certificate', 'address', 'photo']
        widgets = {
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'form_level': forms.TextInput(attrs={'class': 'form-control'}),
            'certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class SchoolTeacherForm(forms.ModelForm):
    class Meta:
        model = SchoolTeacher
        fields = ['teacher', 'school', 'date_of_commitment']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'date_of_commitment': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TeachingForm(forms.ModelForm):
    class Meta:
        model = Teaching
        fields = ['teacher', 'subject', 'total_hours']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        # def __init__(self, *args, **kwargs):
        #     teacher_id = kwargs.pop('teacher_id', None)
        #     super().__init__(*args, **kwargs)
        #     if teacher_id:
        #         self.fields['subject'].queryset = Subject.objects.filter(teaching__teacher_id=teacher_id)


class StudyClassForm(forms.ModelForm):
    class Meta:
        model = StudyClass
        fields = ['name', 'designation', 'option']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'option': forms.Select(attrs={'class': 'form-control'}),
        }


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['date_course', 'start_time', 'end_time', 'teacher', 'subject',
                  'study_class', 'classroom', 'coefficient']
        widgets = {
            'date_course': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'study_class': forms.Select(attrs={'class': 'form-control'}),
            'classroom': forms.Select(attrs={'class': 'form-control'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']
        fields = ['lastname', 'firstname', 'date_of_birth', 'gender', 'phone', 'birth_certificate', 'document', 'photo',
                  'school']
        widgets = {
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        exclude = ['user']
        fields = ['lastname', 'firstname', 'date_of_birth',
                  'gender', 'phone', 'job', 'position', 'formation',
                  'address', 'photo', 'study_level'
                  ]
        widgets = {
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'job': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'formation': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'study_level': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ParentingForm(forms.ModelForm):
    class Meta:
        model = Parenting
        fields = ['family_bond', 'tutor']
        widgets = {
            # 'parent': forms.Select(attrs={'class': 'form-control'}),
            # 'student': forms.Select(attrs={'class': 'form-control'}),
            'family_bond': forms.Select(attrs={'class': 'form-control'}),
            'tutor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['last_school', 'last_study_class', 'study_class', 'date_enrollment']
        widgets = {
            'last_school': forms.Select(attrs={'class': 'form-control'}),
            'last_study_class': forms.Select(attrs={'class': 'form-control'}),
            'study_class': forms.Select(attrs={'class': 'form-control'}),
            'date_enrollment': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['designation', 'type_exam',
                  'date_exam', 'subject',]
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'type_exam': forms.Select(attrs={'class': 'form-control'}),
            'date_exam': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }


class StudentExamForm(forms.ModelForm):
    class Meta:
        model = StudentExam
        fields = ['student', 'exam', 'grade']

        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['type', 'status', 'date',
                  'justified', 'student',
                  'teacher', 'course'
                  ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'justified': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['year', 'description', 'courses', 'school']
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'courses': forms.Select(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }
