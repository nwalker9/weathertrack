from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import WeatherRecord, City
from .forms import WeatherRecordForm

def home(request):
    city_count = City.objects.count()
    record_count = WeatherRecord.objects.count()

    return render(request, 'myapp/home.html', {
        'city_count': city_count,
        'record_count': record_count
    })

def record_list(request):
    records = WeatherRecord.objects.select_related('city').all()

    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myapp/list.html', {
        'page_obj': page_obj
    })

def record_detail(request, pk):
    record = get_object_or_404(WeatherRecord, pk=pk)

    return render(request, 'myapp/detail.html', {
        'record': record
    })

def record_create(request):
    if request.method == 'POST':
        form = WeatherRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = WeatherRecordForm()

    return render(request, 'myapp/form.html', {'form': form})

def record_delete(request, pk):
    record = get_object_or_404(WeatherRecord, pk=pk)

    if request.method == 'POST':
        record.delete()
        return redirect('record_list')

    return render(request, 'myapp/confirm_delete.html', {
        'record': record
    })

def about(request):
    return render(request, "core/about.html")

"""class TaskListView(ListView):
    model = Task
    template_name = "core/task_list.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(is_done=True)"""


"""class TaskDetailView(DetailView):
    model = Task
    template_name = "core/task_detail.html"
    context_object_name = 'task'   """ 