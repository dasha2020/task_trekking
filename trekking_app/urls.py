from django.urls import path
from .views import *


urlpatterns = [
    path('home/', ViewAllTasks.as_view(), name='home'),
]