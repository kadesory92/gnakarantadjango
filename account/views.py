# Dans votre fichier views.py

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import EmployeeForm, UserForm, FounderForm


def login(request):
    return render(request, 'auth/login.html')


def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.role = 'ADMIN'
            user.save()
    else:
        user_form = UserForm()
    return render(request, 'auth/register.html', {'user_form': user_form})


def register_founder(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        founder_form = FounderForm(request.POST, request.FILES)
        if user_form.is_valid() and founder_form.is_valid():
            # Save the user with the FOUNDER role
            user = user_form.save(commit=False)
            user.role = 'FOUNDER'
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

    return render(request, 'auth/register_founder.html', {'user_form': user_form, 'founder_form': founder_form})


def register_employee(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST, request.FILES)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            return redirect('admin-dashboard')
    else:
        user_form = UserForm()
        employee_form = EmployeeForm()

    return render(request, 'auth/register_employee.html', {
        'user_form': user_form,
        'employee_form': employee_form
    })