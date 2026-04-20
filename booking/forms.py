from django import forms
from .models import Car, Booking

# 1. Форма додавання автомобіля
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year', 'vin']
        widgets = {
            'make': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: Toyota'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: Camry'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2020'}),
            'vin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '17 символів VIN-коду'}),
        }

# 2. Форма запису на СТО
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['car', 'service', 'date', 'time']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        # Отримуємо користувача, щоб показати ТІЛЬКИ його автомобілі
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['car'].queryset = Car.objects.filter(owner=user)