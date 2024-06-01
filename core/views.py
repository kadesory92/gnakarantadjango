from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def school_dashboard(request):
    return render(request, 'core/school/dashboard.html')



