from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from account.decorators import role_required
from account.forms import FounderForm, UserForm
from core.models import Student
from school.forms import SchoolForm, LocalForm
from school.models import Founder, Local, School, Staff


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
    schools = School.objects.all()

    # Filtering
    query = request.GET.get('q')
    direction_query = request.GET.get('direction')
    ire_query = request.GET.get('ire')
    type_query = request.GET.get('type')

    if query:
        schools = schools.filter(name__icontains=query)
    if direction_query:
        schools = schools.filter(direction__name__icontains=direction_query)
    if ire_query:
        schools = schools.filter(ire__name__icontains=ire_query)
    if type_query:
        schools = schools.filter(type__icontains=type_query)

    # Pagination
    paginator = Paginator(schools, 10)  # Show 10 services per page
    page = request.GET.get('page')
    try:
        schools = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, display the first page
        schools = paginator.page(1)
    except EmptyPage:
        # If the page is out of bounds (for example, 9999), display the last results page
        schools = paginator.page(paginator.num_pages)

    context = {
        'schools': schools,
        'query': query,
        'direction_query': direction_query,
        'ire_query': ire_query,
        'type_query': type_query
    }
    return render(request, 'school/admin_school/list_school.html', context)


def detail_school(request, id):
    try:
        school = get_object_or_404(School, pk=id)
        # staff = Staff.objects.filter(school=school)
        # student = Student.objects.filter(school=school)
    except Http404:
        return render(request, 'school/admin_school/detail_school.html', {
            'error_message': "School don't exist !"
        })
    return render(request, 'school/admin_school/detail_school.html', {'school': school})


def delete_school(request, id):
    school = get_object_or_404(School, pk=id)
    if request.method == 'POST':
        school.delete()
        return redirect('manage_school')
    return render(request, 'school/admin_school/school_confirm_delete.html', {'school': school})


def edit_school(request, id):
    school = get_object_or_404(School, pk=id)

    if request.method == 'POST':
        school_form = SchoolForm(request.POST, request.FILES, instance=school)
        if school_form.is_valid():
            school_form.save()
            messages.success(request, "Les informations de l'école ont été mise à jpur avec succès")
            return redirect('manage_school')
        else:
            messages.error(request, "Une erreur est survenue lors de la mise à jour !")
    else:
        school_form = SchoolForm(instance=school)
    return render(request, 'school/admin_school/edit_school.html')


def manage_school(request):
    return render(request, 'school/admin_school/manage_school.html')


def create_local(request):
    local_form = LocalForm(request.POST)
    if request.method == 'POST':
        if local_form.is_valid():
            local_form.save()
            return redirect('manage_school')
        else:
            local_form = LocalForm()
    return render(request, 'school/admin_school/create_local.html', {'local_form': local_form})


def local_detail(request, id):
    try:
        local = get_object_or_404(request, pk=id)
    except Http404:
        return render(request, 'school/admin_school/local_detail.html', {
            'error_message': "Le local demandé n'existe pas.",
        })
    return render(request, 'school/admin_school/local_detail.html', {
        'local': local
    })


def delete_local(request, id):
    local = get_object_or_404(Local, pk=id)
    if request.method == 'POST':
        local.delete()
        return redirect('list_local')
    return render(request, 'school/admin_school/local_confirm_delete.html', {'local': local})


def edit_local(request):
    return render(request, '')


def create_staff(request):
    return render(request, '')


def manage_staff(request):
    return render(request, '')
