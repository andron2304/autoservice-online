from django.db import models
from django.contrib.auth.models import User

# 1. Каталог послуг
class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва послуги")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна (грн)")

    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"

    def __str__(self):
        return f"{self.name} ({self.price} грн)"

# 2. Гараж клієнта (Автомобілі)
class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Власник")
    make = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Рік випуску")
    vin = models.CharField(max_length=17, unique=True, verbose_name="VIN-код")

    class Meta:
        verbose_name = "Автомобіль"
        verbose_name_plural = "Автомобілі"

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

# 3. Майстри / Бокси
class Master(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я майстра або назва боксу")
    
    class Meta:
        verbose_name = "Майстер/Бокс"
        verbose_name_plural = "Майстри та Бокси"

    def __str__(self):
        return self.name

# 4. Система бронювання (Записи)
class Booking(models.Model):
    # Статуси згідно з твоїм ТЗ
    STATUS_CHOICES = [
        ('pending', 'Очікує підтвердження'),
        ('in_progress', 'В роботі'),
        ('done', 'Готово'),
        ('cancelled', 'Скасовано'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клієнт")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобіль")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, verbose_name="Послуга")
    master = models.ForeignKey(Master, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Майстер")
    date = models.DateField(verbose_name="Дата запису")
    time = models.TimeField(verbose_name="Час запису")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    class Meta:
        verbose_name = "Запис"
        verbose_name_plural = "Записи"
        ordering = ['-date', '-time'] # Сортування від найновіших

    def __str__(self):
        return f"{self.date} {self.time} | {self.car} - {self.service}"