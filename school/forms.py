from django import forms
from .models import School, Local, Staff


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ['user']
        fields = [
            'founder', 'direction', 'ire', 'name', 'category',
            'level', 'phone', 'address_email', 'site_web', 'image'
        ]
        widgets = {
            # 'user': forms.HiddenInput(),
            'founder': forms.Select(attrs={'class': 'form-control'}),
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'ire': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'site_web': forms.URLInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['school', 'designation', 'type', 'category', 'address']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['user']
        fields = [
            'lastname', 'firstname', 'date_of_birth', 'gender', 'phone',
            'position', 'formation', 'address', 'photo', 'certificate', 'school'
        ]
        widgets = {
            # 'user': forms.HiddenInput(),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'formation': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'certificate': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }
