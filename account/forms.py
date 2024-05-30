from django import forms

from service.models import Employee
from .models import User
from school.models import Founder


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }


# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'password': forms.TextInput(attrs={'class': 'form-control'})
#         }


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class FounderForm(forms.ModelForm):
    class Meta:
        model = Founder
        exclude = ['user']
        widgets = {
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'date': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user']
        widgets = {
            'lastname': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control mb-2', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control mb-2'}),
            'phone': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'position': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'status': forms.Select(attrs={'class': 'form-control mb-2'}),
            'formation': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'address': forms.Textarea(attrs={'class': 'form-control custom-textarea mb-2', 'row': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control mb-2'}),
            'certificate': forms.FileInput(attrs={'class': 'form-control mb-2'}),
            'service': forms.Select(attrs={'class': 'form-control mb-2'}),
        }
