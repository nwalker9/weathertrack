import json
import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from .models import WeatherRecord, City, Player
from .forms import WeatherRecordForm


def home(request):
    record_count = WeatherRecord.objects.count()
    player_count = Player.objects.count()
    cities = City.objects.all()
    latest = WeatherRecord.objects.select_related('city')[:5]
    return render(request, 'myapp/home.html', {
        'record_count': record_count,
        'player_count': player_count,
        'cities': cities,
        'latest': latest,
    })

def record_list(request):
    query = request.GET.get('q', '')
    records = WeatherRecord.objects.select_related('city').all()
    if query:
        records = records.filter(city__name__icontains=query)
    paginator = Paginator(records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/list.html', {
        'page_obj': page_obj,
        'query': query,
    })


def record_detail(request, pk):
    record = get_object_or_404(WeatherRecord.objects.select_related('city'), pk=pk)
    return render(request, 'myapp/detail.html', {'record': record})


def record_create(request):
    if request.method == 'POST':
        form = WeatherRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record created successfully.')
            return redirect('record_list')
    else:
        form = WeatherRecordForm()
    return render(request, 'myapp/form.html', {'form': form, 'title': 'Add record'})


def record_update(request, pk):
    record = get_object_or_404(WeatherRecord, pk=pk)
    if request.method == 'POST':
        form = WeatherRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully.')
            return redirect('record_detail', pk=pk)
    else:
        form = WeatherRecordForm(instance=record)
    return render(request, 'myapp/form.html', {'form': form, 'title': 'Edit record'})


def record_delete(request, pk):
    record = get_object_or_404(WeatherRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Record deleted.')
        return redirect('record_list')
    return render(request, 'myapp/confirm_delete.html', {'record': record})


def analytics(request):
    qs = WeatherRecord.objects.select_related('city').values(
        'city__name', 'date', 'temperature_max', 'temperature_min',
        'precipitation_sum', 'wind_speed_max'
    )
    df = pd.DataFrame(list(qs))

    if df.empty:
        return render(request, 'myapp/analytics.html', {'no_data': True})

    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)

    # Chart 1 (line): average daily max temp per city over time
    temp_by_city = {}
    for city in df['city__name'].unique():
        city_df = df[df['city__name'] == city].sort_values('date')
        temp_by_city[city] = {
            'labels': city_df['date'].dt.strftime('%Y-%m-%d').tolist(),
            'values': city_df['temperature_max'].tolist(),
        }

    # Chart 2 (bar): average max temp per city
    avg_temp = df.groupby('city__name')['temperature_max'].mean().round(1)
    bar_chart = {
        'labels': avg_temp.index.tolist(),
        'values': avg_temp.values.tolist(),
    }

    # Chart 3 (doughnut): total precipitation per city
    total_precip = df.groupby('city__name')['precipitation_sum'].sum().round(1)
    precip_chart = {
        'labels': total_precip.index.tolist(),
        'values': total_precip.values.tolist(),
    }

    # Summary stats table
    summary = df[['temperature_max', 'temperature_min', 'precipitation_sum', 'wind_speed_max']]\
        .describe().round(2).to_dict()

    return render(request, 'myapp/analytics.html', {
        'temp_by_city_json': json.dumps(temp_by_city),
        'bar_chart_json': json.dumps(bar_chart),
        'precip_chart_json': json.dumps(precip_chart),
        'summary': summary,
        'cities': df['city__name'].unique().tolist(),
    })


@staff_member_required
@require_POST
def fetch_data(request):
    try:
        call_command('fetch_data')
        messages.success(request, 'Data fetched successfully.')
    except Exception as e:
        messages.error(request, f'Fetch failed: {e}')
    return redirect('home')
def player_list(request):
    query = request.GET.get('q', '')
    position = request.GET.get('position', '')
    level = request.GET.get('level', '')

    players = Player.objects.all()

    if query:
        players = players.filter(name__icontains=query)
    if position:
        players = players.filter(club_position__icontains=position)
    if level:
        players = players.filter(player_level=level)

    paginator = Paginator(players, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    levels = Player.objects.values_list('player_level', flat=True).distinct()

    return render(request, 'myapp/player_list.html', {
        'page_obj': page_obj,
        'query': query,
        'position': position,
        'level': level,
        'levels': levels,
    })


def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'myapp/player_detail.html', {'player': player})


def player_analytics(request):
    from django.db.models import Avg

    qs = Player.objects.values(
        'club_position', 'player_level', 'age',
        'rating', 'speed', 'strength', 'dribbling', 'ball_control'
    )
    df = pd.DataFrame(list(qs))

    if df.empty:
        return render(request, 'myapp/player_analytics.html', {'no_data': True})

    # Chart 1 (bar): average speed by position
    avg_speed = df.groupby('club_position')['speed'].mean().round(1).sort_values(ascending=False).head(10)
    speed_chart = {
        'labels': avg_speed.index.tolist(),
        'values': avg_speed.values.tolist(),
    }

    # Chart 2 (scatter data): dribbling vs ball control
    scatter_data = df[['dribbling', 'ball_control']].dropna().sample(min(500, len(df))).to_dict('records')

    # Chart 3 (line): average speed and strength by age
    age_df = df.groupby('age')[['speed', 'strength']].mean().round(1).sort_index()
    age_chart = {
        'labels': age_df.index.tolist(),
        'speed': age_df['speed'].tolist(),
        'strength': age_df['strength'].tolist(),
    }

    # Chart 4 (doughnut): player level distribution
    level_counts = df['player_level'].value_counts()
    level_chart = {
        'labels': level_counts.index.tolist(),
        'values': level_counts.values.tolist(),
    }

    # Summary stats
    stats_df = df[['rating', 'speed', 'strength', 'dribbling', 'ball_control']].describe().round(2)
    stat_labels = {'count': 'Count', 'mean': 'Mean', 'min': 'Min', 'max': 'Max', 'std': 'Std dev'}
    stats_rows = []
    for stat in ['count', 'mean', 'min', 'max', 'std']:
        row = stats_df.loc[stat]
        stats_rows.append({
            'label':        stat_labels[stat],
            'rating':       row['rating'],
            'speed':        row['speed'],
            'strength':     row['strength'],
            'dribbling':    row['dribbling'],
            'ball_control': row['ball_control'],
        })

    return render(request, 'myapp/player_analytics.html', {
        'speed_chart_json':   json.dumps(speed_chart),
        'scatter_json':       json.dumps(scatter_data),
        'age_chart_json':     json.dumps(age_chart),
        'level_chart_json':   json.dumps(level_chart),
        'stats_rows':         stats_rows,
    })
