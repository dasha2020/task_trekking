from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    statuses = [
        ('is_done', 'Done'),
        ('in_progress', 'In progress'),
        ('not_done', 'Not Done'),
    ]
    priorities = [
        ('urgent', 'Urgent'),
        ('not_urgent', 'Not Urgent'),
    ]
    
    title = models.CharField(max_length=100)  
    description = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=statuses, default='not_done')
    priority = models.CharField(max_length=15, choices=priorities, default='not_urgent')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)



