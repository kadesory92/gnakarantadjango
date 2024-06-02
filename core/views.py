from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from account.decorators import has_role, role_required
from account.forms import UserForm
from core.forms import TeacherForm, StudentForm, EnrollmentForm, SchoolTeacherForm, SubjectForm, StudyClassForm, \
    TeachingForm
from core.models import Student, Teacher, SchoolTeacher, Subject, StudyClass, Enrollment
from school.models import School
from service.models import Employee


def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def school_dashboard(request):
    return render(request, 'core/school/dashboard.html')


# GESION DES PROFESSEUR


@login_required
def manage_teacher(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    teachers = Teacher.objects.filter(direction__school=school)

    # Filtrage et recherche
    query = request.GET.get('q')
    gender_filter = request.GET.get('gender')
    status_filter = request.GET.get('status')

    if query:
        teachers = teachers.filter(Q(firstname__icontains=query) | Q(lastname__icontains=query))

    if gender_filter:
        teachers = teachers.filter(gender=gender_filter)

    if status_filter:
        teachers = teachers.filter(status=status_filter)

    context = {
        'school': school,
        'teachers': teachers,
    }

    return render(request, 'core/school/teacher/manage_teacher.html', context)


@login_required(login_url='login')
@role_required(['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE'])
def register_teacher(request):
    # if not has_role(request.user, ['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE']):
    #     return redirect('home')  # Rediriger si l'utilisateur n'a pas les droits

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        teacher_form = TeacherForm(request.POST, request.FILES)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()

            return redirect('teacher_list')  # Rediriger vers la liste des enseignants ou une autre page
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()

    return render(request, 'service/admin/teacher/register_teacher.html', {
        'user_form': user_form,
        'teacher_form': teacher_form
    })


def detail_teacher(request):
    return render(request, 'core/school/teacher/edit_teacher.html')


@login_required
def edit_teacher(request, pk):
    if not has_role(request.user, ['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE']):
        return redirect('home')
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher_form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if teacher_form.is_valid():
            teacher_form.save()
            return redirect('detail_teacher', pk=teacher.pk)
    else:
        teacher_form = TeacherForm(instance=teacher)
    return render(request, 'edit_teacher.html', {'teacher_form': teacher_form, 'teacher': teacher})


@login_required
def delete_teacher(request, pk):
    if not has_role(request.user, ['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE']):
        return redirect('home')
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'delete_teacher.html', {'teacher': teacher})


@login_required
@role_required('SCHOOL')
def assign_teacher(request):
    if request.method == 'POST':
        form = SchoolTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_teacher', school_id=form.cleaned_data['school'].id)
    else:
        form = SchoolTeacherForm()
    return render(request, 'assign_teacher.html', {'form': form})


def un_assign_teacher(request, school_teacher_id):
    school_teacher = get_object_or_404(SchoolTeacher, id=school_teacher_id)
    if request.method == 'POST':
        school_teacher.delete()
        return redirect('manage_teacher', school_id=school_teacher.school.id)
    return render(request, 'un_assign_teacher.html', {'school_teacher': school_teacher})


# GESTION DES MATIERES


@login_required
def list_subject(request):
    subjects = Subject.objects.all()
    return render(request, 'subject_list.html', {'subjects': subjects})


@login_required
def create_subject(request):
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST)
        if subject_form.is_valid():
            subject_form.save()
            return redirect('subject_list')
    else:
        subject_form = SubjectForm()
    return render(request, 'subject_form.html', {'subject_form': subject_form})


@login_required
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST, instance=subject)
        if subject_form.is_valid():
            subject_form.save()
            return redirect('subject_list')
    else:
        subject_form = SubjectForm(instance=subject)
    return render(request, 'subject_form.html', {'subject_form': subject_form})


@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('subject_list')
    return render(request, 'subject_confirm_delete.html', {'subject': subject})


@login_required
def create_studyClass(request):
    if request.method == 'POST':
        studyClass = SubjectForm(request.POST)
        if studyClass.is_valid():
            studyClass.save()
            return redirect('subject_list')
    else:
        studyClass = StudyClassForm()
    return render(request, 'class_form.html', {'studyClass': studyClass})


@login_required
def edit_studyClass(request, pk):
    studyClass = get_object_or_404(StudyClass, pk=pk)
    if request.method == 'POST':
        studyClass_form = StudyClassForm(request.POST, instance=studyClass)
        if studyClass_form.is_valid():
            studyClass_form.save()
            return redirect('subject_list')
    else:
        studyClass_form = StudyClassForm(instance=studyClass)
    return render(request, 'subject_form.html', {'studyClass_form': studyClass_form})


@login_required
def delete_studyClass(request, pk):
    studyClass = get_object_or_404(StudyClass, pk=pk)
    if request.method == 'POST':
        studyClass.delete()
        return redirect('list_classes')
    return render(request, 'class_confirm_delete.html', {'studyClass': studyClass})


def create_teaching(request):
    if request.method == 'POST':
        teaching_form = TeachingForm(request.POST)
        if teaching_form.is_valid():
            teaching_form.save()
            return redirect('success_page')  # Rediriger vers une page de succès
    else:
        teaching_form = TeachingForm()
    return render(request, 'teaching_form.html', {'form': teaching_form})


@login_required(login_url='login')
def create_student(request):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour ajouter un étudiant
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    try:
        # Récupérer l'école liée à l'utilisateur connecté
        if user.role == 'SCHOOL':
            school = School.objects.get(user=user)
        else:
            employee = Employee.objects.get(user=user)
            school = employee.service  # Assuming employee is linked to a service, update if necessary

        if request.method == 'POST':
            student_form = StudentForm(request.POST, request.FILES)

            if student_form.is_valid():
                student = student_form.save(commit=False)
                student.school = school
                student.save()

                # Stocker l'ID de l'étudiant dans la session pour le récupérer dans la vue suivante
                request.session['student_id'] = student.id

                return redirect('create_parent')  # Rediriger vers le formulaire d'enregistrement de parent

        else:
            student_form = StudentForm()

        context = {
            'student_form': student_form,
        }

        return render(request, 'core/school/student/create_student.html', context)

    except Employee.DoesNotExist:
        raise PermissionDenied


@login_required(login_url='login')
def enroll_student(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect(
            'create_student')  # Rediriger vers la création de l'étudiant si l'ID de l'étudiant n'est pas trouvé

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect('create_student')  # Rediriger vers la création de l'étudiant si l'étudiant n'est pas trouvé

    if request.method == 'POST':
        enrollment_form = EnrollmentForm(request.POST)

        if enrollment_form.is_valid():
            enrollment = enrollment_form.save(commit=False)
            enrollment.student = student
            enrollment.school = student.school
            enrollment.date_enrollment = timezone.now()
            enrollment.save()

            # Nettoyer l'ID de l'étudiant de la session après l'inscription
            del request.session['student_id']

            return redirect('service_dashboard')  # Rediriger vers le tableau de bord après l'inscription

    else:
        enrollment_form = EnrollmentForm()

    context = {
        'enrollment_form': enrollment_form,
        'student': student,
    }

    return render(request, 'core/school/enroll_student.html', context)


@login_required
def transfer_student(request, student_id):
    # Récupérer l'élève à transférer
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        # Récupérer l'ID de la nouvelle école à partir du formulaire
        new_school_id = request.POST.get('new_school')
        new_school = get_object_or_404(School, pk=new_school_id)

        # Récupérer l'inscription de l'élève dans l'école actuelle
        current_enrollment = Enrollment.objects.get(student=student, school=student.school)

        # Créer une nouvelle inscription pour la nouvelle école
        new_enrollment = Enrollment.objects.create(
            student=student,
            school=new_school,
            last_school=student.school,  # Garder une trace de l'école précédente
            last_study_class=current_enrollment.study_class,
            study_class=current_enrollment.study_class,  # Peut être modifié si nécessaire
            date_enrollment=date.today()  # Date d'inscription à la nouvelle école
        )

        # Mettre à jour l'inscription de l'élève dans l'école actuelle
        current_enrollment.delete()

        # Rediriger vers la page de détails de l'élève
        return redirect('detail_student', student_id=student.id)

    else:
        # Récupérer toutes les écoles disponibles (sauf l'école actuelle de l'élève)
        available_schools = School.objects.exclude(pk=student.school.pk)

    return render(request, 'service/admin/student/transfer_student.html',
                  {'student': student, 'available_schools': available_schools})
