from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_buses, name='search_buses'),
    path('reserve/', views.reserve_seats, name='reserve_seats'),
    path('reservations/', views.view_reservations, name='view_reservations'),
]
