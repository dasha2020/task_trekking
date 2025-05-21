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
from .forms import TaskForm, CustomUserCreationForm, LoginForm
from collections import defaultdict

# Create your views here.

class TaskFormView(LoginRequiredMixin, FormView):
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
        #context = self.get_context_data(tasks=tasks, popup=True)
        view_name = request.resolver_match.view_name

        if self.task and view_name == 'edit_task':
            form = TaskForm(initial=self.get_initial())
            context = self.get_context_data(task=self.task, tasks=tasks, form=form, popup=True)
        elif self.task and view_name == 'delete_task':
            print("DEBUG: Deleting task")
            context = self.get_context_data(tasks=tasks, popup_delete=True)
        elif view_name == 'add_task':
            print("DEBUG: Adding task")
            form = TaskForm()
            context = self.get_context_data(task=self.task, tasks=tasks, form=form, popup=True)
        else:
            context = self.get_context_data(tasks=tasks)

        
        context["css_file"] = 'styles.css'
        return render(request, "home.html", context)
    
    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST or 'cancel_delete' in request.POST:
            #tasks = Task.objects.all()
            #context = self.get_context_data(tasks=tasks, popup=False)
            #context["css_file"] = 'styles.css'
            #return render(request, 'home.html', context)
            return redirect("home")
        if 'delete' in request.POST:
            self.action = "delete"
            self.task.delete()
            return redirect("home")
        if 'save' in request.POST:
            self.action = "edit"
        if 'add' in request.POST:
            self.action = "add"

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if self.action == "add" or self.action == "edit":
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']
            priority = form.cleaned_data['priority']
            deadline = form.cleaned_data['deadline']

        if self.task and self.action == "edit":
            self.task.title = title
            self.task.description = description
            self.task.status = status
            self.task.priority = priority
            self.task.deadline = deadline
            self.task.save()
        elif self.task and self.action == "delete":
            self.task.delete()
            return redirect("home")
        elif self.action == "add":
            Task.objects.create(title=title, description=description, status=status, priority=priority, deadline=deadline)

        #tasks = Task.objects.all()
        #context = self.get_context_data(tasks=tasks, popup=False)
        #context["css_file"] = 'styles.css'
        #return render(self.request, 'home.html', context)
        return redirect("home")


class ViewAllTasks(LoginRequiredMixin, View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        context["form"] = TaskForm()
        return context
    
    def get(self, request, task_id=None):
        user = request.user
        if request.path == reverse('filter'):
            tasks = Task.objects.all()
            tasks = tasks.filter(user=user)
            status = request.GET.get('status')
            priority = request.GET.get('priority')
            if status or priority:
                if status == "All" and priority == "All":
                    context = self.get_context_data(tasks=tasks)
                    return render(request, 'home.html', context)
                elif status != "All" and priority == "All":
                    tasks = tasks.filter(status=status)
                    context = self.get_context_data(tasks=tasks)
                    return render(request, 'home.html', context)
                elif status == "All" and priority != "All":
                    tasks = tasks.filter(priority=priority)
                    context = self.get_context_data(tasks=tasks)
                    return render(request, 'home.html', context)
                elif status != "All" and priority != "All":
                    tasks = tasks.filter(priority=priority)
                    tasks = tasks.filter(status=status)
                    context = self.get_context_data(tasks=tasks)
                    return render(request, 'home.html', context)

        tasks = Task.objects.all()
        tasks = Task.objects.filter(user=user)
        context = self.get_context_data(tasks=tasks)
        return render(request, 'home.html', context)


class ViewAllBoards(LoginRequiredMixin, View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context
    
    def get(self, request, user_id=None):
        tasks = Task.objects.select_related('user')
        user = request.user
    
        #sorted_tasks = defaultdict(list)
        #for task in tasks:
            #sorted_tasks[task.user].append(task)
        user_list = []
        for task in tasks: 
            if task.user != user:
                user_list.append(task.user)

        #user_list = list({task.user for task in tasks})
        print(user_list)
        context = self.get_context_data(user_list=user_list)
        return render(request, 'boards.html', context)

class ViewUserBoard(LoginRequiredMixin, View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context
    
    def get(self, request, user_id=None):
        self.user_id = request.get('user_id')
        if self.user_id:
            another_user = User.objects.get(id=self.user_id)
            tasks = Task.objects.filter(user_id=self.user_id)
        user = request.user

        context = self.get_context_data(tasks=tasks, username=another_user.username)
        return render(request, 'another_user_board.html', context)


#<a href="{% url 'look_into_board' user_id=user.id %}" class="openpopup">More</a>
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(self.request, user)
                return super().form_valid(form)
            else:
                form.add_error(None, 'Password or email incorrect')
        except user is None:
            form.add_error(None, 'User not found')
        return self.form_invalid(form)

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

