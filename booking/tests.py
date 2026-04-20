from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Service, Car, Master, Booking
from datetime import date, time
from decimal import Decimal

class AutoServiceFullTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Створюємо базові дані для тестів
        self.user = User.objects.create_user(username='testclient', password='password123')
        self.service = Service.objects.create(name='Заміна мастила', description='Опис', price=Decimal('1500.00'))
        self.master = Master.objects.create(name='Іван (Бокс 1)')
        self.car = Car.objects.create(owner=self.user, make='Toyota', model='Camry', year=2020, vin='1234567890ABCDEFG')

    # --- 1. ТЕСТИ МОДЕЛЕЙ (База даних) ---
    def test_car_and_booking_models(self):
        car = Car.objects.get(vin='1234567890ABCDEFG')
        self.assertEqual(car.make, 'Toyota')
        
        booking = Booking.objects.create(
            client=self.user, car=self.car, service=self.service,
            master=self.master, date=date(2026, 5, 1), time=time(14, 30)
        )
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(booking.status, 'pending')

    # --- 2. ТЕСТИ МАРШРУТИЗАЦІЇ (Публічні сторінки) ---
    def test_public_pages_load(self):
        # Додали 'booking:' до кожного reverse
        response = self.client.get(reverse('booking:index'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('booking:login'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('booking:register'))
        self.assertEqual(response.status_code, 200)

    # --- 3. ТЕСТИ ДОСТУПУ (Захищені сторінки) ---
    def test_private_pages_protection(self):
        response = self.client.get(reverse('booking:profile'))
        self.assertEqual(response.status_code, 302) 

        response = self.client.get(reverse('booking:add_car'))
        self.assertEqual(response.status_code, 302)

    def test_private_pages_for_logged_user(self):
        self.client.login(username='testclient', password='password123')
        response = self.client.get(reverse('booking:profile'))
        self.assertEqual(response.status_code, 200)

    # --- 4. ТЕСТИ ФОРМ ТА ДІЙ (Функціонал) ---
    def test_user_registration(self):
        response = self.client.post(reverse('booking:register'), {
            'username': 'new_user',
            'password': 'newpassword123',
            'password_confirm': 'newpassword123'
        })
        self.assertIn(response.status_code, [200, 302]) 

    def test_add_car_post(self):
        self.client.login(username='testclient', password='password123')
        response = self.client.post(reverse('booking:add_car'), {
            'make': 'BMW',
            'model': 'X5',
            'year': 2021,
            'vin': 'BMW1234567890ABCD'
        })
        self.assertEqual(Car.objects.count(), 2)