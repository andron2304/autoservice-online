from django.shortcuts import render, redirect
from .models import Service, Vehicle
from .services import create_booking

def service_list(request):
    """Список усіх послуг СТО"""
    services = Service.objects.all()
    return render(request, 'booking/service_list.html', {'services': services})

def book_appointment(request):
    """Обробка форми бронювання"""
    if request.method == 'POST':
        # Спрощена логіка отримання даних з форми
        service_id = request.POST.get('service')
        vehicle_id = request.POST.get('vehicle')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        service = Service.objects.get(id=service_id)
        vehicle = Vehicle.objects.get(id=vehicle_id)
        
        booking = create_booking(request.user, vehicle, service, date, time)
        
        if booking:
            return render(request, 'booking/success.html')
        else:
            return render(request, 'booking/error.html', {'message': 'Цей час уже зайнятий'})
            
    return render(request, 'booking/book_form.html')
from django.shortcuts import render, redirect
from .models import Service, Vehicle
from .services import create_appointment_service

def home(request):
    """Головна сторінка зі списком послуг"""
    services = Service.objects.all()
    return render(request, 'booking/index.html', {'services': services})

def book_service(request):
    """Логіка обробки форми бронювання"""
    if request.method == 'POST':
        # Припустимо, дані приходять з форми
        # Для повноцінної роботи тут зазвичай використовують Django Forms
        service = Service.objects.get(id=request.POST.get('service_id'))
        vehicle = Vehicle.objects.get(id=request.POST.get('vehicle_id'))
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        result = create_appointment_service(request.user, vehicle, service, date, time)
        
        if result:
            return redirect('success_page')
    return render(request, 'booking/book.html')