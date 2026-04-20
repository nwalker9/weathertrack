from django import forms
from .models import WeatherRecord
 
 
class WeatherRecordForm(forms.ModelForm):
    class Meta:
        model = WeatherRecord
        fields = ['city', 'date', 'temperature_max', 'temperature_min',
                  'precipitation_sum', 'wind_speed_max', 'source']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'temperature_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'precipitation_sum': forms.NumberInput(attrs={'class': 'form-control'}),
            'wind_speed_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'source': forms.Select(attrs={'class': 'form-control'}),
        }
 
    def clean(self):
        cleaned_data = super().clean()
        temp_max = cleaned_data.get('temperature_max')
        temp_min = cleaned_data.get('temperature_min')
        if temp_max is not None and temp_min is not None:
            if temp_min > temp_max:
                raise forms.ValidationError(
                    'Minimum temperature cannot be greater than maximum temperature.'
                )
        return cleaned_data