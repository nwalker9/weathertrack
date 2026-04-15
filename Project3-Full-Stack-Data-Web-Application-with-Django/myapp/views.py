from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Task

# from django.http import HttpResponse

# # Create your views here.
# def home(request):
#     return HttpResponse("Hello, Django!")


# def home(request):
#     context = {"message" : "This came from the view"}
#     return render(request, "core/home.html", context)

def home(request):
    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")

def items(request):
    data = [{"name": "Notebook", "category": "Supplies", "price": 2.99},
            {"name": "Mouse", "category": "Electronics", "price": 12.99},
            {"name": "Bottle", "category": "Accessories", "price": 8.25},
            ]
    return render(request, "core/items.html", {"items": data})



def students(request):
    data = [{"name": "Ava", "major": "CS", "GPA": 3.99},
            {"name": "Aidan", "major": "Math", "GPA": 3.4} ]
    return render(request, "core/students.html", {"student_data":data})


class TaskListView(ListView):
    model = Task
    template_name = "core/task_list.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(is_done=True)


class TaskDetailView(DetailView):
    model = Task
    template_name = "core/task_detail.html"
    context_object_name = 'task'    