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
from .forms import TaskForm, CustomUserCreationForm, LoginForm, TaskAnotherUserForm, CommentForm
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
        self.user = request.user
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

        tasks = Task.objects.filter(user_id=self.user.id)
        view_name = request.resolver_match.view_name
        comment = CommentForm()
        comments = Comment.objects.filter(task=self.task, reply__isnull=True)

        if not comments:
            comments = "No comments"

        if self.task and view_name == 'edit_task':
            form = TaskForm(initial=self.get_initial())
            context = self.get_context_data(task=self.task, tasks=tasks, form=form, popup=True, comments=comments, comment=comment)
        elif self.task and view_name == 'delete_task':
            context = self.get_context_data(tasks=tasks, popup_delete=True)
        elif view_name == 'add_task':
            form = TaskForm()
            comments = "No comments"
            context = self.get_context_data(task=self.task, tasks=tasks, form=form, popup=True, comments=comments, comment=comment)
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
        
        id = request.POST.get("id")
        if self.task and 'comment_added' in request.POST:
            comment = CommentForm(request.POST)
            user = request.user
            if comment.is_valid():
                Comment.objects.create(
                    text=comment.cleaned_data['text'],
                    user=user,
                    task=self.task
                )
                return redirect('edit_task', task_id = self.task_id)
        
        elif 'edit' in request.POST and id:
            try:
                comment = Comment.objects.get(id=id, user=request.user)
                if comment.user == request.user:
                    comment.text = request.POST.get('text')
                    comment.save()
            except Comment.DoesNotExist:
                pass
            return redirect('edit_task', task_id=self.task_id)

        elif 'delete' in request.POST and id:
            comment = Comment.objects.get(id=id, user=request.user)
            if comment.user == request.user:
                comment.delete()
            return redirect('edit_task', task_id=self.task_id)

        elif 'reply' in request.POST and id:
            comment = Comment.objects.get(id=id)
            tex = "@" + comment.user.username + " " + request.POST.get('text')
            new_comment = Comment.objects.create(
                text=tex,
                user=request.user,
                task=self.task,
                reply = comment
            )

            return redirect('edit_task', task_id=self.task_id)

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
            Task.objects.create(title=title, description=description, status=status, priority=priority, deadline=deadline, user=self.user)

        #tasks = Task.objects.all()
        #context = self.get_context_data(tasks=tasks, popup=False)
        #context["css_file"] = 'styles.css'
        #return render(self.request, 'home.html', context)
        return redirect("home")

class ViewTaskBoard(LoginRequiredMixin, FormView):
    form_class = TaskAnotherUserForm
    success_url = "/look_into_board/"
    template_name = "another_user_board.html"

    def dispatch(self, request, *args, **kwargs):
        self.task_id = kwargs.get('task_id')
        self.task = None
        if self.task_id:
            self.task = Task.objects.get(id=self.task_id)
            self.user = self.task.user
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
        tasks = Task.objects.filter(user_id=self.user.id)
        #context = self.get_context_data(tasks=tasks, popup=True)
        view_name = request.resolver_match.view_name
        comment = CommentForm()
        comments = Comment.objects.filter(task=self.task, reply__isnull=True)
        if not comments:
            comments = "No comments"

        if self.task and view_name == 'detailed_task':
            form = TaskForm(initial=self.get_initial())
            task_author = []
            if comments != "No comments":
                for c in comments:
                    if c.user == self.user:
                        task_author.append(c.id)

            context = self.get_context_data(task=self.task, tasks=tasks, form=form, popup=True, username=self.user.username, user_id=self.user.id, comment=comment, comments=comments, task_author=task_author, user=self.request.user)
        else:
            context = self.get_context_data(tasks=tasks, form=form, popup=True, username=self.user.username, user_id=self.user.id, comment=comment, user=self.request.user)

        
        context["css_file"] = 'styles.css'
        return render(request, "another_user_board.html", context)
    
    def post(self, request, *args, **kwargs):
        id = request.POST.get("id")
        if 'cancel' in request.POST:
            return redirect("look_into_board", user_id=self.user.id)
        if self.task and 'comment_added' in request.POST:
            comment = CommentForm(request.POST)
            user = request.user
            if comment.is_valid():
                Comment.objects.create(
                    text=comment.cleaned_data['text'],
                    user=user,
                    task=self.task
                )
                return redirect('detailed_task', task_id = self.task_id)
        elif 'edit' in request.POST and id:
            try:
                comment = Comment.objects.get(id=id, user=request.user)
                if comment.user == request.user:
                    comment.text = request.POST.get('text')
                    comment.save()
            except Comment.DoesNotExist:
                pass
            return redirect('detailed_task', task_id=self.task_id)

        elif 'delete' in request.POST and id:
            comment = Comment.objects.get(id=id, user=request.user)
            if comment.user == request.user:
                comment.delete()
            return redirect('detailed_task', task_id=self.task_id)

        return super().post(request, *args, **kwargs)


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
            if 'reset_filter' in request.GET:
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
        user_list = []
        for task in tasks: 
            if task.user != user:
                if task.user not in user_list:
                    user_list.append(task.user)
        print(user_list)
        context = self.get_context_data(user_list=user_list)
        return render(request, 'boards.html', context)

class ViewUserBoard(LoginRequiredMixin, View):
    def get_context_data(self, **kwargs):
        context = kwargs
        context["css_file"] = 'styles.css'
        return context
    
    def get(self, request, user_id=None):
        self.user_id = user_id
        tasks = []
        self.another_user = None
        if self.user_id:
            self.another_user = User.objects.get(id=self.user_id)
            print(self.another_user)
            tasks = Task.objects.filter(user_id=self.user_id)
        
        status = request.GET.get('status')
        priority = request.GET.get('priority')

        if status or priority: 
            if status == "All" and priority == "All":
                context = self.get_context_data(tasks=tasks, username=self.another_user.username, user_id=self.user_id)
                return render(request, 'another_user_board.html', context)
            elif status != "All" and priority == "All":
                tasks = tasks.filter(status=status)
                context = self.get_context_data(tasks=tasks, username=self.another_user.username, user_id=self.user_id)
                return render(request, 'another_user_board.html', context)
            elif status == "All" and priority != "All":
                tasks = tasks.filter(priority=priority)
                context = self.get_context_data(tasks=tasks, username=self.another_user.username, user_id=self.user_id)
                return render(request, 'another_user_board.html', context)
            elif status != "All" and priority != "All":
                tasks = tasks.filter(priority=priority)
                tasks = tasks.filter(status=status)
                context = self.get_context_data(tasks=tasks, username=self.another_user.username, user_id=self.user_id)
                return render(request, 'another_user_board.html', context)
        
        if 'reset_filter' in request.GET:
            context = self.get_context_data(tasks=tasks, username=self.another_user.username, user_id=self.user_id)
            return render(request, 'another_user_board.html', context)

            

        context = self.get_context_data(tasks=tasks, username=self.another_user.username, user_id=self.user_id)
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

