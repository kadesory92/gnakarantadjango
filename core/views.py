from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404

from core.forms import SubjectForm, StudyClassForm, \
    TeachingForm, ClassroomForm, CourseForm
from core.models import Subject, StudyClass, Classroom, Course, Student, SchoolTeacher, Attendance
from school.models import School, Staff
from service.models import Employee


def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def school_dashboard(request):
    user = request.user

    query = request.GET.get('q')
    page_number = request.GET.get('page', 1)

    if user.role in ['SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        staff = get_object_or_404(Staff, user=user)
        school = staff.school
    else:
        school = get_object_or_404(School, user=user)

    students = Student.objects.filter(school=school).order_by('lastname')
    school_teachers = SchoolTeacher.objects.filter(school=school).select_related('teacher')

    student_numbers = students.count()
    teacher_numbers = school_teachers.count()
    staff_numbers = Staff.objects.filter(school=school).count()

    teachers = [school_teacher.teacher for school_teacher in school_teachers]

    if query:
        students = students.filter(
            Q(lastname__icontains=query) |
            Q(firstname__icontains=query) |
            Q(date_of_birth__icontains=query) |
            Q(phone__icontains=query)
        )

    paginator = Paginator(students, 10)  # Afficher 10 étudiants par page
    page_obj = paginator.get_page(page_number)

    # Calcul des présences et des absences
    attendance = Attendance.objects.filter(student__in=students)
    total_attendance = attendance.count()
    present_count = attendance.filter(status='present').count()
    absent_count = attendance.filter(status='absent').count()

    if total_attendance > 0:
        present_percentage = (present_count / total_attendance) * 100
        absent_percentage = (absent_count / total_attendance) * 100
    else:
        present_percentage = 0
        absent_percentage = 0

    context = {
        'school': school,
        'students': page_obj,
        'teachers': teachers,
        'student_numbers': student_numbers,
        'teacher_numbers': teacher_numbers,
        'staff_numbers': staff_numbers,
        'present_percentage': present_percentage,
        'absent_percentage': absent_percentage,
        'query': query,
        'page_obj': page_obj
    }

    return render(request, 'core/school/school_dashboard.html', context)


# SUBJECT MANAGEMENT


@login_required(login_url='login')
def list_subject(request):
    user = request.user
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
    if user.role in ['SCHOOL', 'TEACHER', 'STUDENT']:
        return render(request, 'core/school/subject/list_subject.html', context)
    else:
        return render(request, 'service/admin/subject/list_subjects.html', context)


@login_required(login_url='login')
def create_subject(request):
    if request.method == 'POST':
        subject_form = SubjectForm(request.POST)
        if subject_form.is_valid():
            subject_form.save()
            return redirect('list_subject')
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


def manage_studyClass(request):
    return render(request, '')


@login_required(login_url='login')
def ours_classes(request):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour gérer les classes
    if user.role not in ['SCHOOL_ADMIN', 'SCHOOL_MANAGER', 'SCHOOL']:
        raise PermissionDenied

    # Récupérer l'école liée à l'utilisateur connecté
    if user.role == 'SCHOOL':
        school = School.objects.get(user=user)
    else:
        staff = Staff.objects.get(user=user)
        school = staff.school

    # Initialisez les critères de recherche et de filtrage
    search_query = request.GET.get('search', '')

    #
    # study_classes = StudyClass.objects.filter(school=school).annotate(student_count=Count('students')).filter(
    #     student_count__gt=0).order_by('name')
    classes = StudyClass.objects.filter(current_class__school=school)
    if search_query:
        classes = classes.filter(Q(name__icontains=search_query) | Q(designation__icontains=search_query))

    # Ajouter la pagination
    paginator = Paginator(classes, 10)  # 10 classes par page
    page_number = request.GET.get('page')
    classes_page = paginator.get_page(page_number)

    context = {
        'classes': classes_page,
        'search_query': search_query,
    }

    return render(request, 'core/school/class/ours_classes.html', context)


@login_required(login_url='login')
def create_studyClass(request):
    if request.method == 'POST':
        studyClass_form = StudyClassForm(request.POST)
        if studyClass_form.is_valid():
            studyClass_form.save()
            return redirect('manage_class')
    else:
        studyClass_form = StudyClassForm()
    return render(request, 'service/admin/class/create_class.html', {'studyClass_form': studyClass_form})


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
        staff = Staff.objects.get(user=user)
        school = staff.school

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


@login_required
def manage_course(request):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour gérer les salles de classe
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    # Récupérer l'école liée à l'utilisateur connecté
    if user.role == 'SCHOOL':
        school = School.objects.get(user=user)
    else:
        staff = Staff.objects.get(user=user)
        school = staff.school

    query = request.GET.get('q', '')
    courses = Course.objects.filter(study_class__school=school)

    if query:
        courses = courses.filter(
            Q(subject__name__icontains=query) |
            Q(teacher__lastname__icontains=query) |
            Q(study_class__name__icontains=query)
        )

    paginator = Paginator(courses, 10)  # 10 cours par page
    page = request.GET.get('page')
    courses = paginator.get_page(page)

    return render(request, 'core/school/course/manage_course.html', {'courses': courses, 'query': query})


@login_required
def create_course(request):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour gérer les salles de classe
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    # Récupérer l'école liée à l'utilisateur connecté
    if user.role == 'SCHOOL':
        school = School.objects.get(user=user)
    else:
        staff = Staff.objects.get(user=user)
        school = staff.school

    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course = course_form.save()
            course.school = school
            course.save()
            return redirect('manage_course')
    else:
        course_form = CourseForm()
    return render(request, 'core/school/course/create_course.html', {'course_form': course_form})


@login_required
def detail_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'core/school/course/detail_course.html', {'course': course})


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course_form = CourseForm(request.POST, instance=course)
        if course_form.is_valid():
            course_form.save()
            return redirect('manage_course')
    else:
        course_form = CourseForm(instance=course)
    return render(request, 'core/school/course/edit_course.html', {'course_form': course_form})


@login_required
def list_course_by_class(request, study_class_id):
    study_class = get_object_or_404(StudyClass, pk=study_class_id)
    query = request.GET.get('q', '')
    courses = Course.objects.filter(study_class=study_class).order_by('date_course')

    if query:
        courses = courses.filter(
            Q(subject__name__icontains=query) |
            Q(teacher__lastname__icontains=query)
        )

    paginator = Paginator(courses, 10)  # 10 cours par page
    page = request.GET.get('page')
    courses = paginator.get_page(page)

    return render(request, 'core/school/course/list_course_by_class.html',
                  {'courses': courses, 'study_class': study_class, 'query': query})


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('manage_course')
    return render(request, 'core/school/course/delete_course.html', {'course': course})
