from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.service_list, name='service_list'),
    path('book/', views.book_service, name='book_service'),
    path('add-car/', views.add_car, name='add_car'), # <--- Додали цей рядок
    path('profile/', views.profile, name='profile'),
    
    # Авторизація та реєстрація
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='booking:index'), name='logout'),
]