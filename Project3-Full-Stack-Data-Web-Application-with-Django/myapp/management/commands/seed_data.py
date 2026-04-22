import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from myapp.models import City, WeatherRecord, DataRun


CITIES_META = {
    'Tallahassee': {'latitude': 30.4383, 'longitude': -84.2807},
    'Miami':       {'latitude': 25.7617, 'longitude': -80.1918},
    'Atlanta':     {'latitude': 33.7490, 'longitude': -84.3880},
}

CSV_PATH = Path(__file__).resolve().parents[3] / 'data' / 'raw' / 'weather_data.csv'


class Command(BaseCommand):
    help = 'Load weather CSV data from Project 2 into the database'

    def handle(self, *args, **options):
        if not CSV_PATH.exists():
            self.stderr.write(f'CSV not found at {CSV_PATH}')
            return

        # Create city objects
        for name, coords in CITIES_META.items():
            City.objects.get_or_create(
                name=name,
                defaults={'latitude': coords['latitude'], 'longitude': coords['longitude']}
            )
        self.stdout.write('Cities ready.')

        created = 0
        skipped = 0

        with open(CSV_PATH, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    city = City.objects.get(name=row['city'])
                    _, was_created = WeatherRecord.objects.get_or_create(
                        city=city,
                        date=row['date'],
                        defaults={
                            'temperature_max':   float(row['temperature_max'])   if row['temperature_max']   else None,
                            'temperature_min':   float(row['temperature_min'])   if row['temperature_min']   else None,
                            'precipitation_sum': float(row['precipitation_sum']) if row['precipitation_sum'] else 0.0,
                            'wind_speed_max':    float(row['wind_speed_max'])    if row['wind_speed_max']    else 0.0,
                            'source': 'csv',
                        }
                    )
                    if was_created:
                        created += 1
                    else:
                        skipped += 1
                except Exception as e:
                    self.stderr.write(f'Error on row {row}: {e}')

        self.stdout.write(f'Done — {created} created, {skipped} skipped (already existed).')
