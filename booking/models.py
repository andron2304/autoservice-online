from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Власник")
    make = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Рік випуску")
    vin_code = models.CharField(max_length=17, unique=True, verbose_name="VIN-код")

    class Meta:
        verbose_name = "Автомобіль"
        verbose_name_plural = "Автомобілі"

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва послуги")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Вартість (грн)")
    duration_minutes = models.IntegerField(verbose_name="Тривалість (у хвилинах)")

    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('in_progress', 'В роботі'),
        ('completed', 'Виконано'),
        ('cancelled', 'Скасовано'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клієнт")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="Автомобіль")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, verbose_name="Послуга")
    date = models.DateField(verbose_name="Дата запису")
    time = models.TimeField(verbose_name="Час запису")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    class Meta:
        verbose_name = "Запис на сервіс"
        verbose_name_plural = "Записи на сервіс"
        ordering = ['-date', '-time']

    def __str__(self):
        return f"Запис: {self.client.username} - {self.vehicle} на {self.date}"