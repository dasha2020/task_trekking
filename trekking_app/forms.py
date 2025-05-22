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

class CommentForm(forms.Form):
    text = forms.CharField(
        label="Add your comment",
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write your comment here...',
            'rows': 3
        })
    )

class TaskAnotherUserForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
        })
    )

    description = forms.CharField(
        label="Description",
        max_length=300,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
        })
    )

    status = forms.ChoiceField(
        choices=Task.statuses,
        widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly',}),
    )

    priority = forms.ChoiceField(
        choices=Task.priorities,
        widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly',}),
    )

    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'readonly': 'readonly',
        })
    )



class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        help_text="Password must be at least 8 characters and contain numbers, symbols and letters.")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        help_text="Please, confirm your password.")
    
    def clean_password1(self):
        password1 = self.cleaned_data.get("password")
        validate_password(password1)

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user 
