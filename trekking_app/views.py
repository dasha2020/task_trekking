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
from .forms import TaskForm

# Create your views here.

class TaskFormView(FormView):
    form_class = TaskForm
    success_url = "/home/"
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        self.task_id = kwargs.get('task_id')
        self.task = None
        if self.task_id:
            self.task = Task.objects.get(id=self.task_id)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        if self.task:
            return {
                'title': self.task.title,
                'description': self.task.description,
                'status': self.task.status,
                'priority': self.task.priority,
                'deadline': self.task.deadline,
            }
        return super().get_initial()
    
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        context = self.get_context_data(tasks=tasks, popup=True)

        if self.task:
            form = TaskForm(initial=self.get_initial())
        else:
            form = TaskForm()

        context = self.get_context_data(task=self.task, form=form, popup=True)
        context["css_file"] = 'styles.css'
        return render(request, "home.html", context)
    
    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            #tasks = Task.objects.all()
            #context = self.get_context_data(tasks=tasks, popup=False)
            #context["css_file"] = 'styles.css'
            #return render(request, 'home.html', context)
            return redirect("home")

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        status = form.cleaned_data['status']
        priority = form.cleaned_data['priority']
        deadline = form.cleaned_data['deadline']

        if self.task:
            self.task.title = title
            self.task.description = description
            self.task.status = status
            self.task.priority = priority
            self.task.deadline = deadline
            self.task.save()
        else:
            Task.objects.create(title=title, description=description, status=status, priority=priority, deadline=deadline)

        #tasks = Task.objects.all()
        #context = self.get_context_data(tasks=tasks, popup=False)
        #context["css_file"] = 'styles.css'
        #return render(self.request, 'home.html', context)
        return redirect("home")


class ViewAllTasks(View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        context["form"] = TaskForm()
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
            if request.path == reverse('edit_task', kwargs={'task_id': task_id}):
                return self.update(request, task_id)
    
    def update(self, request, task_id):
        task = Task.objects.get(id=task_id)

        if request.method == 'POST':
            if 'cancel' in request.POST:
                tasks = Task.objects.all()
                context = self.get_context_data(tasks=tasks, popup=False)
                return render(request, 'home.html', context)
                
            if 'save' in request.POST:
                task.title = request.POST.get('title')
                task.description = request.POST.get('description')
                task.status = request.POST.get('status')
                task.priority = request.POST.get('priority')
                task.deadline = request.POST.get('deadline')
                task.save()

                tasks = Task.objects.all()
                context = self.get_context_data(tasks=tasks, popup=False)
                return render(request, 'home.html', context)


        context = self.get_context_data(task=task, popup=True)
        return render(request, 'home.html', context)

