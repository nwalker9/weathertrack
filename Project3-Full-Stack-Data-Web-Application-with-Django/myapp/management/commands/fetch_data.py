import time
import requests
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from myapp.models import City, WeatherRecord, DataRun

CITIES_META = {
    'Tallahassee': {'latitude': 30.4383, 'longitude': -84.2807},
    'Miami':       {'latitude': 25.7617, 'longitude': -80.1918},
    'Atlanta':     {'latitude': 33.7490, 'longitude': -84.3880},
}

BASE_URL = 'https://archive-api.open-meteo.com/v1/archive'
MAX_RETRIES = 2


class Command(BaseCommand):
    help = 'Fetch latest weather data from Open-Meteo and save to database'

    def handle(self, *args, **options):
        today = date.today()
        # Fetch the past 4 weeks in 7-day chunks
        for city_name, coords in CITIES_META.items():
            city, _ = City.objects.get_or_create(
                name=city_name,
                defaults={'latitude': coords['latitude'], 'longitude': coords['longitude']}
            )
            total_saved = 0

            for week in range(4):
                end = today - timedelta(days=1 + week * 7)
                start = end - timedelta(days=6)

                params = {
                    'latitude':   coords['latitude'],
                    'longitude':  coords['longitude'],
                    'start_date': start.isoformat(),
                    'end_date':   end.isoformat(),
                    'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max',
                    'timezone': 'auto',
                }

                data = None
                for attempt in range(1, MAX_RETRIES + 1):
                    try:
                        resp = requests.get(BASE_URL, params=params, timeout=10)
                        resp.raise_for_status()
                        data = resp.json()
                        break
                    except requests.exceptions.Timeout:
                        self.stderr.write(f'{city_name}: timeout attempt {attempt}')
                        if attempt < MAX_RETRIES:
                            time.sleep(1.5)
                    except requests.exceptions.RequestException as e:
                        self.stderr.write(f'{city_name}: error attempt {attempt} — {e}')
                        if attempt < MAX_RETRIES:
                            time.sleep(1.5)

                if data is None:
                    self.stderr.write(f'{city_name} [{start}→{end}]: all attempts failed, skipping.')
                    continue

                daily = data.get('daily', {})
                times      = daily.get('time', [])
                temp_max   = daily.get('temperature_2m_max', [])
                temp_min   = daily.get('temperature_2m_min', [])
                precip     = daily.get('precipitation_sum', [])
                wind_speed = daily.get('wind_speed_10m_max', [])

                with transaction.atomic():
                    for i, day in enumerate(times):
                        WeatherRecord.objects.update_or_create(
                            city=city,
                            date=day,
                            defaults={
                                'temperature_max':   temp_max[i]   if i < len(temp_max)   else None,
                                'temperature_min':   temp_min[i]   if i < len(temp_min)   else None,
                                'precipitation_sum': precip[i]     if i < len(precip)     else 0.0,
                                'wind_speed_max':    wind_speed[i] if i < len(wind_speed) else 0.0,
                                'source': 'api',
                            }
                        )
                        total_saved += 1

            DataRun.objects.create(city=city, records_fetched=total_saved, source='api')
            self.stdout.write(f'{city_name}: {total_saved} records saved.')

        self.stdout.write('fetch_data complete.')
