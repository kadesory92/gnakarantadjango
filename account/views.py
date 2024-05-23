# Dans votre fichier views.py

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import EmployeeForm, UserForm, FounderForm


def login(request):
    return render(request, 'auth/login.html')


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
    global user
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, request.FILES)
        if employee_form.is_valid():
            # Create a user associated with the employee
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
            employee = employee_form.save(commit=False)
            employee.user = user  # Associate the created user with the employee
            employee.save()
            messages.success(request, 'Employee account created successfully!')
            return redirect('dashboard')  # Redirect to the dashboard page after the creation of the employee
    else:
        employee_form = EmployeeForm()
    return render(request, 'registration/register_employee.html', {'employee_form': employee_form})
