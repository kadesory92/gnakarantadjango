from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect

from account.decorators import role_required, has_role
from account.forms import UserForm
from core.forms import TeacherForm, TeachingForm, SchoolTeacherForm
from core.models import Teacher, SchoolTeacher
from school.models import School
from service.models import Employee


# GESION DES PROFESSEUR


@login_required(login_url='login')
def manage_teacher_by_school(request):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle requis pour gérer les professeurs
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    # Récupérer l'école liée à l'utilisateur connecté
    if user.role == 'SCHOOL':
        school = School.objects.get(user=user)
    else:
        employee = get_object_or_404(Employee, user=user)
        school = employee.service  # Assumant que l'employé est lié à un service qui représente une école

    # Récupérer les professeurs enseignant dans cette école
    teachers = Teacher.objects.filter(teaching__subject__school=school).distinct()

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

    # Ajouter la pagination
    paginator = Paginator(teachers, 10)  # 10 enseignants par page
    page_number = request.GET.get('page')
    teachers_page = paginator.get_page(page_number)

    context = {
        'school': school,
        'teachers_page': teachers_page,
        'query': query,
        'gender_filter': gender_filter,
        'status_filter': status_filter,
    }

    return render(request, 'core/school/teacher/manage_teacher_by_school.html', context)


@login_required(login_url='login')
def list_teacher(request):
    user = request.user

    # Vérifiez si l'utilisateur a le rôle d'une école
    if user.role != 'SCHOOL':
        raise PermissionDenied

    # Récupérer l'école liée à l'utilisateur connecté
    school = School.objects.get(user=user)

    # Initialisez les critères de recherche et de filtrage
    search_query = request.GET.get('search', '')

    # Filtrer les professeurs par la direction de l'école et par les critères de recherche
    teachers = Teacher.objects.filter(direction=school.direction).order_by('lastname')
    if search_query:
        teachers = teachers.filter(Q(firstname__icontains=search_query) | Q(lastname__icontains=search_query))

    # Ajouter la pagination
    paginator = Paginator(teachers, 10)  # 10 professeurs par page
    page_number = request.GET.get('page')
    teachers_page = paginator.get_page(page_number)

    context = {
        'teachers_page': teachers_page,
        'search_query': search_query,
    }

    return render(request, 'core/school/manage_teacher.html', context)


@login_required(login_url='login')
@role_required(['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE'])
def register_teacher(request):
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

            return redirect('assign_subjects',
                            teacher_id=teacher.id)  # Rediriger vers la page d'attribution des matières
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()

    return render(request, 'service/admin/teacher/register_teacher.html', {
        'user_form': user_form,
        'teacher_form': teacher_form
    })


@role_required(['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE'])
def assign_subjects(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        teaching_form = TeachingForm(request.POST)
        if teaching_form.is_valid():
            teaching = teaching_form.save(commit=False)
            teaching.teacher = teacher
            teaching.save()
            return redirect('teacher_list')  # Rediriger vers la liste des enseignants ou une autre page appropriée
    else:
        teaching_form = TeachingForm(initial={'teacher': teacher})

    return render(request, 'service/admin/teacher/assign_subjects.html', {
        'teacher': teacher,
        'teaching_form': teaching_form
    })


@login_required(login_url='login')
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
@role_required(['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE'])
def delete_teacher(request, pk):
    if not has_role(request.user, ['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE']):
        return redirect('home')
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        return redirect('teacher_list')
    return render(request, 'delete_teacher.html', {'teacher': teacher})


@login_required(login_url='login')
@role_required(['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE', 'SCHOOL'])
def assign_teacher(request):
    if request.method == 'POST':
        form = SchoolTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_teacher', school_id=form.cleaned_data['school'].id)
    else:
        form = SchoolTeacherForm()
    return render(request, 'assign_teacher.html', {'form': form})


@login_required(login_url='login')
@role_required(['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE', 'SCHOOL'])
def un_assign_teacher(request, school_teacher_id):
    school_teacher = get_object_or_404(SchoolTeacher, id=school_teacher_id)
    if request.method == 'POST':
        school_teacher.delete()
        return redirect('manage_teacher', school_id=school_teacher.school.id)
    return render(request, 'un_assign_teacher.html', {'school_teacher': school_teacher})
