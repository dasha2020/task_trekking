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
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context
    
    def get(self, request, task_id=None):
        if request.path == reverse('filter'):
            tasks = Task.objects.all()
            status = request.GET.get('status')
            priority = request.GET.get('priority')
            if status:
                if status != "All":
                    tasks = tasks.filter(status=status)
                    context = self.get_context_data(tasks=tasks)
                else:
                    context = self.get_context_data(tasks=tasks)
                return render(request, 'home.html', context)
            if priority:
                if priority != "All":
                    tasks = tasks.filter(priority=priority)
                    context = self.get_context_data(tasks=tasks)
                else:
                    context = self.get_context_data(tasks=tasks)
                return render(request, 'home.html', context)
        tasks = Task.objects.all()
        context = self.get_context_data(tasks=tasks)
        return render(request, 'home.html', context)
    def post(self, request, task_id=None):
        if request.path == reverse('add_task'):
            title = request.POST.get('title')
            description = request.POST.get('description')
            status = request.POST.get('status')
            priority = request.POST.get('priority')
            deadline = request.POST.get('deadline')

            task = Task(title=title, description=description, status=status, priority=priority, deadline=deadline)

            try:
                task.save()
                messages.success(request, 'Task created successfully!')
            except IntegrityError as e:
                messages.error(request, f"Error: {str(e)}")

            tasks = Task.objects.all()
            context = self.get_context_data(tasks=tasks)
            return render(request, 'home.html', context)
        
        elif task_id:
            if request.path == reverse('edit_student', kwargs={'task_id': task_id}):
                return self.update(request, task_id)
    
    def update(self, request, task_id):
        task = Task.objects.get(id=task_id)

        if request.method == 'POST':
            task.title = request.POST.get('title')
            task.description = request.POST.get('description')
            task.status = request.POST.get('status')
            task.priority = request.POST.get('priority')
            task.deadline = request.POST.get('deadline')
            task.save()

            return HttpResponseRedirect(reverse('home'))

        context = self.get_context_data(task=task, popup=True)
        return render(request, 'home.html', context)

