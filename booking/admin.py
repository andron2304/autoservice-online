from django.contrib import admin
from .models import Vehicle, Service, Appointment

admin.site.register(Vehicle)
admin.site.register(Service)
admin.site.register(Appointment)