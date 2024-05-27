from django.contrib import messages
from django.shortcuts import render, redirect

from account.forms import FounderForm


def create_founder(request):
    if request.method == 'POST':
        founder_form = FounderForm(request.POST)
        if founder_form.is_valid():
            founder = founder_form.save()
            user = request.is_authenticated
            founder.user = user
            founder.save()
            messages.success('request', 'Service created successfully!')
            return redirect('home')
    else:
        founder_form = FounderForm()
    return render(request, 'school/founder/create_founder.html', {'founder_form': founder_form})


def create_school(request):
    return render(request, 'school/admin_school/create_school.html')
