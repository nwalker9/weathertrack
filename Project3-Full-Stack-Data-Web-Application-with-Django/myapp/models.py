from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
 
 
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
 
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'cities'
 
    def __str__(self):
        return self.name
 
 
class WeatherRecord(models.Model):
    SOURCE_CHOICES = [
        ('csv', 'CSV Import'),
        ('api', 'API Fetch'),
    ]
 
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    temperature_max = models.FloatField(
        validators=[MinValueValidator(-60), MaxValueValidator(60)]
    )
    temperature_min = models.FloatField(
        validators=[MinValueValidator(-60), MaxValueValidator(60)]
    )
    precipitation_sum = models.FloatField(default=0.0)
    wind_speed_max = models.FloatField(default=0.0)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='csv')
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['-date']
        unique_together = ['city', 'date']
 
    def __str__(self):
        return f"{self.city.name} — {self.date}"
 
 
class DataRun(models.Model):
    run_timestamp = models.DateTimeField(auto_now_add=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='runs')
    records_fetched = models.IntegerField(default=0)
    source = models.CharField(max_length=10, choices=WeatherRecord.SOURCE_CHOICES, default='api')
 
    class Meta:
        ordering = ['-run_timestamp']
 
    def __str__(self):
        return f"{self.city.name} — {self.run_timestamp:%Y-%m-%d %H:%M}"

class Player(models.Model):
    LEVEL_CHOICES = [
        ('Elite', 'Elite'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Bronze', 'Bronze'),
    ]

    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    national_position = models.CharField(max_length=50, blank=True, null=True)
    club = models.CharField(max_length=100)
    club_position = models.CharField(max_length=50, blank=True, null=True)
    rating = models.IntegerField()
    height = models.CharField(max_length=20, blank=True, null=True)
    weight = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField()
    skill_moves = models.IntegerField(default=0)
    ball_control = models.FloatField(default=0)
    dribbling = models.FloatField(default=0)
    speed = models.FloatField(default=0)
    strength = models.FloatField(default=0)
    player_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Bronze')

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return f"{self.name} ({self.club})"
