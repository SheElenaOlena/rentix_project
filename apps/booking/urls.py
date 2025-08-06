from django.urls import path
from .views import (
    BookingCreateView,
    BookingCancelView,
    BookingActionView,
    FilteredBookingsView
)

urlpatterns = [
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
    path('bookings/<int:pk>/action/', BookingActionView.as_view(), name='booking-action'),
    path('bookings/', FilteredBookingsView.as_view(), name='booking-list'),
]
