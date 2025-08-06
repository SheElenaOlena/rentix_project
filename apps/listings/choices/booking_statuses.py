from enum import Enum

class BookingStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    REJECTED = 'rejected'

    @classmethod
    def choices(cls):
        return [(status.value, status.name.capitalize()) for status in cls]