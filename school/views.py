from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from account.decorators import role_required
from account.forms import FounderForm, UserForm
from school.forms import SchoolForm
from school.models import Founder


# def create_founder(request):
#     if request.method == 'POST':
#         founder_form = FounderForm(request.POST)
#         if founder_form.is_valid():
#             founder = founder_form.save()
#             user = request.is_authenticated
#             founder.user = user
#             founder.save()
#             messages.success('request', 'Service created successfully!')
#             return redirect('home')
#     else:
#         founder_form = FounderForm()
#     return render(request, 'school/founder/create_founder.html', {'founder_form': founder_form})


@login_required
@role_required(['ADMIN', 'ADMIN_DPE', 'ADMIN_DCE', 'FOUNDER'])
def create_school(request):
    user = request.user

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        school_form = SchoolForm(request.POST, request.FILES)
        if school_form.is_valid():
            school = school_form.save(commit=False)
            # Set the school type and founder based on the user's role
            if user.role == 'FOUNDER':
                school.type = 'private'
                school.founder = Founder.objects.get(user=user)
            else:
                school.type = 'public'
                school.founder = None

            user = user_form.save(commit=False)
            user.save()

            school.user = user
            school.save()
            return redirect('home')
    else:
        user_form = UserForm()
        school_form = SchoolForm()

    return render(request, 'school/admin_school/create_school.html',
                  {'school_form': school_form, 'user_form': user_form})


def list_schools(request):
    return render(request, '')


def manage_school(request):
    return render(request, 'school/admin_school/manage_school.html')
