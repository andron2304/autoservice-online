from django.contrib.auth.decorators import login_required
from .forms import CarForm, BookingForm
from django.shortcuts import render, redirect
from .models import Service, Car, Booking

def index(request):
    """Головна сторінка"""
    return render(request, 'booking/index.html')

def service_list(request):
    """Список усіх послуг СТО"""
    services = Service.objects.all() # Беремо реальні послуги з бази даних
    return render(request, 'booking/service_list.html', {'services': services})

@login_required(login_url='/login/')
def add_car(request):
    """Додавання авто в гараж клієнта"""
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user # Прив'язуємо авто до поточного клієнта
            car.save()
            return redirect('booking:book_service') # Після додавання кидаємо на запис
    else:
        form = CarForm()
    return render(request, 'booking/add_car.html', {'form': form})

@login_required(login_url='/login/')
@login_required(login_url='/login/')
def book_service(request):
    # Отримуємо ID послуги з посилання (якщо воно передано)
    service_id = request.GET.get('service_id')
    
    if not Car.objects.filter(owner=request.user).exists():
        return redirect('booking:add_car')

    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.save()
            return redirect('booking:profile')
    else:
        # Якщо service_id передано, підставляємо цю послугу у форму за замовчуванням
        initial_data = {}
        if service_id:
            initial_data['service'] = service_id
        
        form = BookingForm(user=request.user, initial=initial_data)
        
    return render(request, 'booking/book_form.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Service, Car, Booking

# ... твої попередні функції (index, service_list, book_service) залишаються тут ...

def register(request):
    """Реєстрація нового клієнта"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Одразу авторизуємо після реєстрації
            return redirect('booking:index')
    else:
        form = UserCreationForm()
    
    return render(request, 'booking/register.html', {'form': form})

@login_required(login_url='/login/')
def profile(request):
    """Кабінет клієнта: його авто та записи"""
    cars = Car.objects.filter(owner=request.user)
    # Сортуємо записи: спочатку найновіші
    bookings = Booking.objects.filter(client=request.user).order_by('-date', '-time')
    return render(request, 'booking/profile.html', {'cars': cars, 'bookings': bookings})