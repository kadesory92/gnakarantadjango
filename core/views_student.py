from datetime import date

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from account.forms import UserForm
from core.forms import StudentForm, EnrollmentForm, ParentForm, ParentingForm
from core.models import Student, Enrollment, Parent
from school.models import School, Staff
from service.models import Employee


@login_required(login_url='login')
def manage_student(request):
    user = request.user

    # Check if the user has the required role to manage students
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    # Initialize the search and filtering criteria
    search_query = request.GET.get('search', '')

    # Retrieve the school linked to the logged-in user
    if user.role == 'SCHOOL':
        school = School.objects.get(user=user)
    else:
        staff = Staff.objects.get(user=user)
        school = staff.school  # Assuming employee is linked to a service, update if necessary

    # Filter students by school through enrollments and by search criteria
    enrollments = Enrollment.objects.filter(school=school).select_related('student')
    if search_query:
        enrollments = enrollments.filter(
            Q(student__firstname__icontains=search_query) |
            Q(student__lastname__icontains=search_query) |
            Q(student__phone__icontains=search_query)
        )

    students = [enrollment.student for enrollment in enrollments]

    # Add pagination
    paginator = Paginator(students, 10)  # 10 students per page
    page_number = request.GET.get('page')
    students_page = paginator.get_page(page_number)

    context = {
        'students_page': students_page,
        'search_query': search_query,
    }

    return render(request, 'core/school/student/manage_student.html', context)


@login_required(login_url='login')
def create_student(request):
    user = request.user

    # Check if the user has the required role to add a student
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    try:
        # Retrieve the school linked to the logged-in user
        if user.role == 'SCHOOL':
            school = School.objects.get(user=user)
        else:
            staff = Staff.objects.get(user=user)
            school = staff.school  # Assuming employee is linked to a service, update if necessary

        if request.method == 'POST':
            user_form = UserForm(request.POST)
            student_form = StudentForm(request.POST, request.FILES)

            if student_form.is_valid() and user_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])

                user.save()

                student = student_form.save(commit=False)
                student.user = user
                student.school = school
                student.save()

                # Store the school ID in the session to retrieve it after
                # request.session['school_id'] = school.id

                # Store the student ID in the session to retrieve it in the next view
                # request.session['student_id'] = student.id

                # Store the student ID in a variable to be transmitted to the next page

                student_id = student.id
                return redirect('create_parent', student_id)  # Redirect to the parent registration form

        else:
            user_form = UserForm()
            student_form = StudentForm()

        context = {
            'user_form': user_form,
            'student_form': student_form,
        }

        return render(request, 'core/school/student/create_student.html', context)

    except Employee.DoesNotExist:
        raise PermissionDenied


@login_required(login_url='login')
def detail_student(request, student_id):
    user = request.user

    # Check if the user has the required role to view a student's details
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

    # Check if the user has the required role to edit a student
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

    # Check if the user has the required role to delete a student
    if user.role not in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        raise PermissionDenied

    try:
        student = Student.objects.get(id=student_id, school__user=user)

        if request.method == 'POST':
            student.delete()
            return redirect('student_list')  # Redirect to the list of students after deletion

        context = {
            'student': student,
        }

        return render(request, 'core/school/student/delete_student.html', context)

    except Student.DoesNotExist:
        raise Http404("Student does not exist")


@login_required
def transfer_student(request, student_id):
    # Retrieve the student to be transferred
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        # Retrieve the ID of the new school from the form
        new_school_id = request.POST.get('new_school')
        new_school = get_object_or_404(School, pk=new_school_id)

        # Retrieve the student's registration in the current school
        current_enrollment = Enrollment.objects.get(student=student, school=student.school)

        # Create a new enrollment for the new school
        Enrollment.objects.create(
            student=student,
            school=new_school,
            last_school=student.school,  # Keeping track of the previous school
            last_study_class=current_enrollment.study_class,
            study_class=current_enrollment.study_class,  # Can be modified if necessary
            date_enrollment=date.today()  # Date of registration at the new school
        )

        # Update the student's enrollment in the current school
        current_enrollment.delete()

        # Redirect to the student's details page
        return redirect('detail_student', student_id=student.id)

    else:
        # Retrieve all available schools (except the student's current school)
        available_schools = School.objects.exclude(pk=student.school.pk)

    return render(request, 'service/admin/student/transfer_student.html',
                  {'student': student, 'available_schools': available_schools})


def create_parent(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        parent_form = ParentForm(request.POST, request.FILES)
        if user_form.is_valid() and parent_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            parent = parent_form.save(commit=False)
            parent.user = user
            parent.save()

            # request.session['parent_id'] = parent.id

            return redirect('create_parenting', student_id=student.id, parent_id=parent.id)

    else:
        user_form = UserForm()
        parent_form = ParentForm()

    context = {
        'user_form': user_form,
        'parent_form': parent_form
    }

    return render(request, 'core/school/parent/create_parent.html', context)


def create_parenting(request, student_id, parent_id):
    student = get_object_or_404(Student, id=student_id)
    parent = get_object_or_404(Parent, id=parent_id)
    if request.method == 'POST':
        parenting_form = ParentingForm(request.POST)

        if parenting_form.is_valid():
            parenting = parenting_form.save(commit=False)
            parenting.student = student
            parenting.parent = parent
            parenting.save()

            return redirect('enrollment_student', student_id=student.id)
        # student_id = student.id
    else:
        parenting_form = ParentingForm()

    return render(request, 'core/school/parent/create_parenting.html', {'parenting_form': parenting_form})


@login_required(login_url='login')
def enroll_student(request, student_id):
    # user = request.user

    # if user.role == 'SCHOOL':
    #     school = get_object_or_404(School, user=user)
    #
    # if user.role in ['SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
    #     staff = get_object_or_404(Staff, user=user)
    #     school = staff.school

    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        enrollment_form = EnrollmentForm(request.POST)

        if enrollment_form.is_valid():
            enrollment = enrollment_form.save(commit=False)
            enrollment.student = student
            enrollment.school = student.school
            enrollment.date_enrollment = timezone.now()
            enrollment.save()

            # Clean the session student ID after registration
            # del request.session['student_id']

            return redirect('manage_student')  # Redirect to the dashboard after registration

    else:
        enrollment_form = EnrollmentForm()

    context = {
        'enrollment_form': enrollment_form,
        # 'student': student,
    }

    return render(request, 'core/school/student/enroll_student.html', context)
