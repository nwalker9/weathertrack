import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from myapp.models import Player

CSV_PATH = Path(__file__).resolve().parents[4] / 'data' / 'processed' / 'cleaned_players.csv'


class Command(BaseCommand):
    help = 'Load FIFA player CSV data into the database'

    def handle(self, *args, **options):
        if not CSV_PATH.exists():
            self.stderr.write(f'CSV not found at {CSV_PATH}')
            return

        created = 0
        skipped = 0

        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    _, was_created = Player.objects.get_or_create(
                        name=row['Name'],
                        club=row.get('Club', ''),
                        defaults={
                            'nationality':       row.get('Nationality', ''),
                            'national_position': row.get('National_Position') or None,
                            'club_position':     row.get('Club_Position') or None,
                            'rating':            int(float(row['Rating'])) if row.get('Rating') else 0,
                            'height':            row.get('Height') or None,
                            'weight':            row.get('Weight') or None,
                            'age':               int(float(row['Age'])) if row.get('Age') else 0,
                            'skill_moves':       int(float(row['Skill_Moves'])) if row.get('Skill_Moves') else 0,
                            'ball_control':      float(row['Ball_Control']) if row.get('Ball_Control') else 0,
                            'dribbling':         float(row['Dribbling']) if row.get('Dribbling') else 0,
                            'speed':             float(row['Speed']) if row.get('Speed') else 0,
                            'strength':          float(row['Strength']) if row.get('Strength') else 0,
                            'player_level':      row.get('Player_Level', 'Bronze'),
                        }
                    )
                    if was_created:
                        created += 1
                    else:
                        skipped += 1
                except Exception as e:
                    self.stderr.write(f'Error on row {row.get("Name", "unknown")}: {e}')

        self.stdout.write(f'Done — {created} players created, {skipped} skipped.')
