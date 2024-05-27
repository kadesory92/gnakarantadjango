# Dans votre fichier views.py

from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import EmployeeForm, UserForm, FounderForm
from .models import User


def loginUser(request):
    return render(request, 'auth/login.html')


def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


# def register(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#
#         user_form.fields['role'].choices = [
#             ('ADMIN', 'Administrateur')
#         ]
#
#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password'])
#             # user.role = 'ADMIN'
#             user.save()
#     else:
#         user_form = UserForm()
#
#         user_form.fields['role'].choices = [
#             ('ADMIN', 'Administrateur')
#         ]
#
#     return render(request, 'auth/register.html', {'user_form': user_form})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        # Set the role choices to only ADMIN
        user_form.fields['role'].choices = [
            ('FOUNDER', 'Fondateur'),
            ('ADMIN', 'Administrateur')
        ]

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            # Redirect based on role
            if user.role == 'ADMIN':
                # Check if a user with the role ADMIN already exists
                if User.objects.filter(role='ADMIN').exists():
                    messages.error(request, 'An admin user already exists.')
                    return redirect('register')
                else:
                    user.save()
                    login(request, user)
                    messages.success(request, 'Admin user registered successfully!')
                    return redirect('home')  # Change to your actual admin dashboard URL
            elif user.role == 'FOUNDER':
                user.save()
                login(request, user)
                messages.success(request, 'Founder user registered successfully!')
                return redirect('register_founder')  # Change to your actual founder dashboard URL
        else:
            messages.error(request, 'There was an error in the form. Please correct the errors below.')
    else:
        user_form = UserForm()

        # Set the role choices to only ADMIN
        user_form.fields['role'].choices = [
            ('FOUNDER', 'Fondateur'),
            ('ADMIN', 'Administrateur')
        ]

    return render(request, 'auth/register.html', {'user_form': user_form})


def register_founder(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        founder_form = FounderForm(request.POST, request.FILES)
        # Filter roles for employee registration
        user_form.fields['role'].choices = [
            ('FOUNDER', 'Fondateur Ecole privée')
        ]
        if user_form.is_valid() and founder_form.is_valid():
            # Save the user with the FOUNDER role
            user = user_form.save(commit=False)
            # user.role = 'FOUNDER'
            user.save()

            # Save the founder profile
            founder = founder_form.save(commit=False)
            founder.user = user
            founder.save()
            login(request, user)  # Log in the user immediately after registration (optional)
            return redirect('home')  # Redirect to some view after registration
    else:
        user_form = UserForm()
        founder_form = FounderForm()

        user_form.fields['role'].choices = [
            ('FOUNDER', 'Fondateur Ecole privée')
        ]

    return render(request, 'auth/register_founder.html', {'user_form': user_form, 'founder_form': founder_form})


# def register_employee(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         employee_form = EmployeeForm(request.POST, request.FILES)
#         if user_form.is_valid() and employee_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password'])
#             user.save()
#
#             employee = employee_form.save(commit=False)
#             employee.user = user
#             employee.save()
#
#             messages.success(request, 'Employee registered successfully!')
#
#             return redirect('admin-dashboard')
#         else:
#             messages.error(request, 'There was an error in the form. Please correct the errors below.')
#     else:
#         user_form = UserForm()
#         employee_form = EmployeeForm()
#
#     return render(request, 'auth/register_employee.html', {
#         'user_form': user_form,
#         'employee_form': employee_form
#     })


def register_employee(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST, request.FILES)

        # Filter roles for employee registration
        user_form.fields['role'].choices = [
            ('SERVICE_STAFF', 'Service Staff'),
            ('ADMIN_IRE', 'Admin IRE'),
            ('ADMIN_DPE', 'Admin DPE'),
            ('ADMIN_DCE', 'Admin DCE'),
            ('STAFF_IRE', 'Personnel de IRE'),
            ('STAFF_DCE', 'Personnel de DCE'),
            ('STAFF_DPE', 'Personnel de DPE')
        ]

        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            messages.success(request, 'Employee registered successfully!')
            return redirect('admin-dashboard')
        else:
            messages.error(request, 'There was an error in the form. Please correct the errors below.')
    else:
        user_form = UserForm()
        employee_form = EmployeeForm()

        # Filter roles for employee registration
        user_form.fields['role'].choices = [
            ('SERVICE_STAFF', 'Service Staff'),
            ('ADMIN_IRE', 'Admin IRE'),
            ('ADMIN_DPE', 'Admin DPE'),
            ('ADMIN_DCE', 'Admin DCE'),
            ('STAFF_IRE', 'Personnel de IRE'),
            ('STAFF_DCE', 'Personnel de DCE'),
            ('STAFF_DPE', 'Personnel de DPE')
        ]

    return render(request, 'auth/register_employee.html', {
        'user_form': user_form,
        'employee_form': employee_form
    })


