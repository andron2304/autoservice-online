from django.contrib import admin
from .models import Service, Car, Master, Booking

# 1. Ведення довідника послуг
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    # Які колонки показувати в списку
    list_display = ('name', 'price')
    # Додаємо рядок пошуку по назві
    search_fields = ('name',)
    # Дозволяємо редагувати ціну прямо в таблиці, не заходячи всередину
    list_editable = ('price',)

# Автомобілі (для зручності адміна)
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'vin', 'owner')
    search_fields = ('vin', 'make', 'owner__username')
    list_filter = ('make', 'year')

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name',)

# 2 та 3. Управління розкладом і статусами записів
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Колонки, які побачить адміністратор у загальній таблиці
    list_display = ('date', 'time', 'client', 'car', 'service', 'master', 'status')
    
    # ПАНЕЛЬ ФІЛЬТРІВ справа (вирішує задачу "перегляд на день/тиждень")
    list_filter = ('date', 'status', 'master')
    
    # Зручна шкала навігації по датах зверху таблиці
    date_hierarchy = 'date'
    
    # ДОЗВОЛЯЄ ЗМІНЮВАТИ СТАТУС ТА МАЙСТРА ПРЯМО В ТАБЛИЦІ (без відкриття заявки)
    list_editable = ('status', 'master')
    
    # Сортування: спочатку найновіші
    ordering = ('-date', '-time')