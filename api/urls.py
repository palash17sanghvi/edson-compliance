from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.get_bookings, name='get_bookings'),
]
