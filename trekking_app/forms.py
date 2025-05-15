from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class TaskForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Title',
            'autofocus': 'autofocus',
        })
    )

    description = forms.CharField(
        label="Description",
        max_length=300,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'blablabla'
        })
    )

    status = forms.ChoiceField(
        choices=Task.statuses,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    priority = forms.ChoiceField(
        choices=Task.priorities,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    deadline = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        })
    )
