from django.contrib import admin
from .models import City, WeatherRecord, DataRun, Player
 
 
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display  = ['name', 'latitude', 'longitude']
    search_fields = ['name']
 
 
@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display   = ['city', 'date', 'temperature_max', 'temperature_min',
                      'precipitation_sum', 'wind_speed_max', 'source']
    list_filter    = ['city', 'source']
    search_fields  = ['city__name']
    ordering       = ['-date']
 
 
@admin.register(DataRun)
class DataRunAdmin(admin.ModelAdmin):
    list_display  = ['city', 'run_timestamp', 'records_fetched', 'source']
    list_filter   = ['city', 'source']
    ordering      = ['-run_timestamp']
 
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display  = ['name', 'club', 'club_position', 'rating', 'player_level', 'age']
    list_filter   = ['player_level', 'nationality']
    search_fields = ['name', 'club', 'nationality']
    ordering      = ['-rating']
