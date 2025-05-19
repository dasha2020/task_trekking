from django.urls import path
from .views import *


urlpatterns = [
    path('home/', ViewAllTasks.as_view(), name='home'),
    path('home/', ViewAllTasks.as_view(), name='filter'),
    path('add_task/', TaskFormView.as_view(), name='add_task'),
    path('edit_task/<int:task_id>/', TaskFormView.as_view(), name='edit_task'),
    path('delete_task/<int:task_id>/', TaskFormView.as_view(), name='delete_task'),
]