from django.contrib import admin
from .models import Task, Comment

# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'deadline', 'created_at')
    search_fields = ('title',)
    list_filter = ('status', 'priority',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'text', 'date')
