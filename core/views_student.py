from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from core.forms import StudentForm, EnrollmentForm
from core.models import Student, Enrollment
from school.models import School
from service.models import Employee


@login_required(login_url='login')
def manage_student(request):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour gérer les étudiants
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    # Initialisez les critères de recherche et de filtrage
    search_query = request.GET.get('search', '')
    filter_criteria = request.GET.get('filter', '')

    # Récupérer l'école liée à l'utilisateur connecté
    if user.role == 'SCHOOL':
        school = School.objects.get(user=user)
    else:
        try:
            employee = Employee.objects.get(user=user)
            school = employee.service  # Assuming employee is linked to a service, update if necessary
        except Employee.DoesNotExist:
            raise PermissionDenied

    # Filtrer les étudiants par l'école et par les critères de recherche
    students = Student.objects.filter(school=school).order_by('last_name')
    if search_query:
        students = students.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
    if filter_criteria:
        students = students.filter(study_class_id=filter_criteria)

    # Ajouter la pagination
    paginator = Paginator(students, 10)  # 10 étudiants par page
    page_number = request.GET.get('page')
    students_page = paginator.get_page(page_number)

    # Formulaire de recherche
    search_form = StudentForm(initial={'search': search_query, 'filter': filter_criteria})

    context = {
        'students_page': students_page,
        'search_form': search_form,
    }

    return render(request, 'core/school/student/manage_student.html', context)


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
def detail_student(request, student_id):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour voir les détails d'un étudiant
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    try:
        student = Student.objects.get(id=student_id, school__user=user)

        context = {
            'student': student,
        }

        return render(request, 'core/school/student/detail_student.html', context)

    except Student.DoesNotExist:
        raise Http404("Student does not exist")


@login_required(login_url='login')
def edit_student(request, student_id):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour éditer un étudiant
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    try:
        student = Student.objects.get(id=student_id, school__user=user)

        if request.method == 'POST':
            student_form = StudentForm(request.POST, request.FILES, instance=student)

            if student_form.is_valid():
                student_form.save()
                return redirect('detail_student', student_id=student.id)

        else:
            student_form = StudentForm(instance=student)

        context = {
            'student_form': student_form,
            'student': student,
        }

        return render(request, 'core/school/student/edit_student.html', context)

    except Student.DoesNotExist:
        raise Http404("Student does not exist")


@login_required(login_url='login')
def delete_student(request, student_id):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour supprimer un étudiant
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    try:
        student = Student.objects.get(id=student_id, school__user=user)

        if request.method == 'POST':
            student.delete()
            return redirect('student_list')  # Rediriger vers la liste des étudiants après la suppression

        context = {
            'student': student,
        }

        return render(request, 'core/school/student/delete_student.html', context)

    except Student.DoesNotExist:
        raise Http404("Student does not exist")


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

        # Create a new enrollment for the new school
        Enrollment.objects.create(
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