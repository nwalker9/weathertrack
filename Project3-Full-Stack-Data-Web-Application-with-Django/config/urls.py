from django.urls import path
from . import views
from .views import TaskDetailView, TaskListView

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("items/", views.items, name="items"),
    path("students/", views.students, name="students"),
    path("tasks/", TaskListView.as_view(), name = "task_list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/completed/", TaskListView.as_view(), name="completed_tasks")
]