# Dans votre fichier views.py

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, FounderRegistrationForm, EmployeeForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            role = user_form.cleaned_data['role']
            if role == 'FOUNDER':
                founder_form = FounderRegistrationForm(request.POST, request.FILES)
                if founder_form.is_valid():
                    founder = founder_form.save(commit=False)
                    founder.user = user
                    founder.save()
                    messages.success(request, 'Account created successfully!')
                    return redirect('login')
            else:
                messages.success(request, 'Account created successfully!')
                return redirect('login')
    else:
        user_form = UserRegistrationForm()
        founder_form = FounderRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'founder_form': founder_form})


def register_employee(request):
    global user
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, request.FILES)
        if employee_form.is_valid():
            # Créer un utilisateur associé à l'employé
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()
            employee = employee_form.save(commit=False)
            employee.user = user  # Associer l'utilisateur créé à l'employé
            employee.save()
            messages.success(request, 'Employee account created successfully!')
            return redirect('dashboard')  # Rediriger vers la page de tableau de bord après la création de l'employé
    else:
        employee_form = EmployeeForm()
    return render(request, 'registration/register_employee.html', {'employee_form': employee_form})

