from django import forms
from .models import Task, Checklist, ProductManager, Developer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductManagerForm(forms.ModelForm):
    class Meta:
        model = ProductManager
        fields = ['name']

class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = ['name']
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_link', 'sprint_no']
        widgets = {
            'task_name': forms.TextInput(attrs={'class': 'form-control'}),
            'task_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter task link'}),
            'sprint_no': forms.NumberInput(attrs={'class': 'form-control'}),

        }


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        # exclude created_by and sprint because they are set by view/save
        fields = ['task', 'test_area', 'test_scenario', 'approved_by_PM', 'approved_by_dev', 'status', 'retest_status', 'actual_evidence', 'bug_link', 'remarks']
        widgets = {
            'task': forms.Select(attrs={'class': 'form-select'}),
            'test_area': forms.TextInput(attrs={'class': 'form-control'}),
            'test_scenario': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'approved_by_PM': forms.Select(attrs={'class': 'form-select'}),
            'approved_by_dev': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'retest_status': forms.Select(attrs={'class': 'form-select'}),
            'actual_evidence': forms.URLInput(attrs={'class': 'form-control'}),
            'bug_link': forms.URLInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')