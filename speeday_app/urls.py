# speeday_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('tasks', views.TaskListCreateAPIView.as_view()),
]  