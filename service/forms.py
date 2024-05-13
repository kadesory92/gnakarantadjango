from django import forms
from .models import Service, Employee


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'type_service', 'region', 'commune', 'prefecture', 'sous_prefecture']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type_service': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'commune': forms.TextInput(attrs={'class': 'form-control'}),
            'prefecture': forms.TextInput(attrs={'class': 'form-control'}),
            'sous_prefecture': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmployeeAssignmentForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['service']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'})
        }
