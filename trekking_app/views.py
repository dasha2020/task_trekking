from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from trekking_app.models import Task, Comment
from django.contrib import messages
from django.db import IntegrityError
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
#from .forms import CreateTaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

# Create your views here.

class ViewAllTasks(View):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["css_file"] = 'trekking_app/styles.css'
        return context
    
    def get(self, request):
        tasks = Task.objects.all()
        context = self.get_context_data(tasks=tasks)
        return render(request, 'home.html', context)

