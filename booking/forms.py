from django import forms
from .models import Booking, Car
from django.utils import timezone
from datetime import time

# Форма для додавання автомобіля
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'vin']
        widgets = {
            'make': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: BMW'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: X5'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Форма для запису на послугу з валідацією часу
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['car', 'service', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Показуємо тільки машини цього клієнта
            self.fields['car'].queryset = Car.objects.filter(owner=user)

    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date < timezone.now().date():
            raise forms.ValidationError("Не можна записатися на минулу дату!")
        return booking_date

    def clean_time(self):
        booking_time = self.cleaned_data.get('time')
        booking_date = self.cleaned_data.get('date')
        
        # 1. Робочий графік: з 08:00 до 19:00
        start_work = time(8, 0)
        end_work = time(19, 0)
        
        if not (start_work <= booking_time <= end_work):
            raise forms.ValidationError(f"Ми працюємо з 08:00 до 19:00. Оберіть робочий час.")

        # 2. Перевірка на "вже минулий час" сьогодні
        if booking_date == timezone.now().date():
            now_time = timezone.localtime(timezone.now()).time()
            if booking_time < now_time:
                raise forms.ValidationError("Цей час сьогодні вже минув. Оберіть пізнішу годину.")
        
        return booking_time