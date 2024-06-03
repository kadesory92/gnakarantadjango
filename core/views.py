
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404

from core.forms import SubjectForm, StudyClassForm, \
    TeachingForm, ClassroomForm
from core.models import Subject, StudyClass, Enrollment, Classroom
from school.models import School
from service.models import Employee


def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def school_dashboard(request):
    return render(request, 'core/school/dashboard.html')


# SUBJECT MANAGEMENT


@login_required(login_url='login')
def list_subject(request):
    subjects = Subject.objects.all()
    # Filtrage et recherche
    query = request.GET.get('q')
    if query:
        subjects = subjects.filter(Q(name__icontains=query))

    # Ajouter la pagination
    paginator = Paginator(subjects, 10)  # 10 sujets par page
    page_number = request.GET.get('page')
    subjects_page = paginator.get_page(page_number)

    context = {
        'subjects_page': subjects_page,
        'query': query,
    }

    return render(request, 'service/admin/subject/list_subjects.html', context)


@login_required(login_url='login')
def create_subject(request):
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST)
        if subject_form.is_valid():
            subject_form.save()
            return redirect('subject_list')
    else:
        subject_form = SubjectForm()
    return render(request, 'service/admin/subject/create_subject.html', {'subject_form': subject_form})


@login_required(login_url='login')
def edit_subject(request, id):
    subject = get_object_or_404(Subject, pk=id)
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST, instance=subject)
        if subject_form.is_valid():
            subject_form.save()
            return redirect('subject_list')
    else:
        subject_form = SubjectForm(instance=subject)
    return render(request, 'service/admin/subject/edit_subject.html', {'subject_form': subject_form})


@login_required(login_url='login')
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('subject_list')
    return render(request, 'subject_confirm_delete.html', {'subject': subject})


@login_required(login_url='login')
def create_teaching(request):
    if request.method == 'POST':
        teaching_form = TeachingForm(request.POST)
        if teaching_form.is_valid():
            teaching_form.save()
            return redirect('success_page')  # Rediriger vers une page de succès
    else:
        teaching_form = TeachingForm()
    return render(request, 'teaching_form.html', {'form': teaching_form})


# GESTION DES CLASSES


@login_required(login_url='login')
def manage_studyClass(request):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour gérer les classes
    if user.role not in ['SCHOOL_ADMIN', 'SCHOOL_MANAGER', 'SCHOOL']:
        raise PermissionDenied

    # Récupérer l'école liée à l'utilisateur connecté
    if user.role == 'SCHOOL':
        school = School.objects.get(user=user)
    else:
        employee = Employee.objects.get(user=user)
        school = employee.service

    # Initialisez les critères de recherche et de filtrage
    search_query = request.GET.get('search', '')

    # Filtrer les classes par l'école et par les critères de recherche
    study_classes = StudyClass.objects.filter(school=school).annotate(student_count=Count('students')).filter(student_count__gt=0).order_by('name')
    if search_query:
        study_classes = study_classes.filter(Q(name__icontains=search_query) | Q(designation__icontains=search_query))

    # Ajouter la pagination
    paginator = Paginator(study_classes, 10)  # 10 classes par page
    page_number = request.GET.get('page')
    study_classes_page = paginator.get_page(page_number)

    context = {
        'study_classes_page': study_classes_page,
        'search_query': search_query,
    }

    return render(request, 'core/school/class/manage_class.html', context)


@login_required(login_url='login')
def create_studyClass(request):
    if request.method == 'POST':
        studyClass = SubjectForm(request.POST)
        if studyClass.is_valid():
            studyClass.save()
            return redirect('subject_list')
    else:
        studyClass = StudyClassForm()
    return render(request, 'class_form.html', {'studyClass': studyClass})


@login_required(login_url='login')
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


@login_required(login_url='login')
def detail_studyClass(request, class_id):
    study_class = get_object_or_404(StudyClass, id=class_id)

    return render(request, 'core/school/study_class/detail_class.html', {
        'study_class': study_class
    })


@login_required(login_url='login')
def edit_studyClass(request, class_id):

    study_class = get_object_or_404(StudyClass, id=class_id)

    if request.method == 'POST':
        study_class_form = StudyClassForm(request.POST, instance=study_class)
        if study_class_form.is_valid():
            study_class_form.save()
            return redirect('manage_class')
    else:
        study_class_form = StudyClassForm(instance=study_class)

    return render(request, 'core/school/study_class/edit_class.html', {
        'study_class_form': study_class_form,
        'study_class': study_class
    })


@login_required(login_url='login')
def delete_studyClass(request, class_id):

    study_class = get_object_or_404(StudyClass, id=class_id)

    if request.method == 'POST':
        study_class.delete()
        return redirect('manage_class')

    return render(request, 'core/school/study_class/delete_class.html', {
        'study_class': study_class
    })


@login_required(login_url='login')
def manage_classroom(request):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour gérer les salles de classe
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    # Récupérer l'école liée à l'utilisateur connecté
    if user.role == 'SCHOOL':
        school = School.objects.get(user=user)
    else:
        employee = Employee.objects.get(user=user)
        school = employee.service

    # Initialisez les critères de recherche et de filtrage
    search_query = request.GET.get('search', '')

    # Filtrer les salles de classe par l'école et par les critères de recherche
    classrooms = Classroom.objects.filter(school=school).order_by('name')
    if search_query:
        classrooms = classrooms.filter(Q(name__icontains=search_query) | Q(capacity__icontains=search_query))

    # Ajouter la pagination
    paginator = Paginator(classrooms, 10)  # 10 salles de classe par page
    page_number = request.GET.get('page')
    classrooms_page = paginator.get_page(page_number)

    context = {
        'classrooms_page': classrooms_page,
        'search_query': search_query,
    }

    return render(request, 'core/school/classroom/manage_classroom.html', context)


@login_required(login_url='login')
def create_classroom(request):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour créer une salle de classe
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    # Récupérer l'école liée à l'utilisateur connecté
    if user.role == 'SCHOOL':
        school = School.objects.get(user=user)
    else:
        employee = Employee.objects.get(user=user)
        school = employee.service

    if request.method == 'POST':
        classroom_form = ClassroomForm(request.POST)
        if classroom_form.is_valid():
            classroom = classroom_form.save(commit=False)
            classroom.school = school
            classroom.save()
            return redirect('manage_classroom')
    else:
        classroom_form = ClassroomForm()

    return render(request, 'core/school/classroom/create_classroom.html', {
        'classroom_form': classroom_form
    })


@login_required(login_url='login')
def detail_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)

    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour voir les détails d'une salle de classe
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    # Vérifiez si l'utilisateur appartient à l'école de la salle de classe
    if classroom.school.user != user and not Employee.objects.filter(user=user, service=classroom.school).exists():
        raise PermissionDenied

    return render(request, 'core/school/classroom/detail_classroom.html', {
        'classroom': classroom
    })


@login_required(login_url='login')
def edit_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)

    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour éditer une salle de classe
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    # Vérifiez si l'utilisateur appartient à l'école de la salle de classe
    if classroom.school.user != user and not Employee.objects.filter(user=user, service=classroom.school).exists():
        raise PermissionDenied

    if request.method == 'POST':
        classroom_form = ClassroomForm(request.POST, instance=classroom)
        if classroom_form.is_valid():
            classroom_form.save()
            return redirect('manage_classroom')
    else:
        classroom_form = ClassroomForm(instance=classroom)

    return render(request, 'core/school/classroom/edit_classroom.html', {
        'classroom_form': classroom_form,
        'classroom': classroom
    })


@login_required(login_url='login')
def delete_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)

    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour supprimer une salle de classe
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    # Vérifiez si l'utilisateur appartient à l'école de la salle de classe
    if classroom.school.user != user and not Employee.objects.filter(user=user, service=classroom.school).exists():
        raise PermissionDenied

    if request.method == 'POST':
        classroom.delete()
        return redirect('manage_classroom')

    return render(request, 'core/school/classroom/delete_classroom.html', {
        'classroom': classroom
    })
