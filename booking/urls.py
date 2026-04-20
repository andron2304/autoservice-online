from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.service_list, name='service_list'),
    path('book/', views.book_appointment, name='book_appointment'),
]