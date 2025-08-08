from django.db.models import Q
from apps.listings.models import Listing
from apps.booking.models import Booking


"""фильтрацию по датам и статусу объявления"""
def get_available_listings(check_in, check_out):
    from apps.listings.choices.booking_statuses import BookingStatus
    if check_out <= check_in:
        raise ValueError("Дата выезда должна быть позже даты заезда.")
    # логика пересечения интервалов.
    # только активные объявления
    overlapping_bookings = Booking.objects.filter(
        status=BookingStatus.CONFIRMED,
        check_in__lt=check_out,
        check_out__gt=check_in
    ).values_list('listing_id', flat=True)   #получаем ID занятых объектов.

    listings = Listing.objects.filter(
        is_active=True
    ).exclude(id__in=overlapping_bookings)  #убираем их из списка.

    return listings
