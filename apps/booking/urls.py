from django.urls import path
from .views import (
    BookingCreateView,
    BookingCancelView,
    BookingActionView,
    FilteredBookingsView, BookingDetailView
)

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
    path('<int:pk>/action/', BookingActionView.as_view(), name='booking-action'),
    path('', FilteredBookingsView.as_view(), name='booking-list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
]


#
# Все бронирования	/bookings/
# Только активные	/bookings/?status=active
# Только завершённые	/bookings/?status=past
# По статусу (например, pending)	/bookings/?status=pending
# По конкретному объявлению	/bookings/?listing=3
# По диапазону дат	/bookings/?start=2025-08-01&end=2025-08-31
# Комбинированный фильтр	/bookings/?status=active&listing=2&start=2025-08-01&end=2025-08-31