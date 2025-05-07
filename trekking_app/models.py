from django.db import models

# Create your models here.



class Task(models.Model):
    statuses = [
        ('is_done', 'Done'),
        ('in_progress', 'In progress'),
        ('not_done', 'Not Done'),
    ]
    
    title = models.CharField(max_length=100)  
    description = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=statuses, default='not_done')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.task} - {self.text}"


