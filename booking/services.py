from .models import Appointment

def is_time_slot_available(date, time):
    """Перевіряє, чи не зайнятий цей час іншим клієнтом"""
    return not Appointment.objects.filter(date=date, time=time).exists()

def create_booking(user, vehicle, service, date, time):
    """Сервісний метод для створення запису з перевіркою"""
    if is_time_slot_available(date, time):
        appointment = Appointment.objects.create(
            client=user,
            vehicle=vehicle,
            service=service,
            date=date,
            time=time,
            status='pending'
        )
        return appointment
    return None
from .models import Appointment

def check_time_slot(date, time):
    """Сервіс перевірки: чи немає вже запису на цей час?"""
    return not Appointment.objects.filter(date=date, time=time).exists()

def create_appointment_service(user, vehicle, service, date, time):
    """Бізнес-логіка створення запису"""
    if check_time_slot(date, time):
        return Appointment.objects.create(
            client=user,
            vehicle=vehicle,
            service=service,
            date=date,
            time=time
        )
    return None