from rest_framework import serializers
from .models import Booking
from ..listings.models import Listing
from ..listings.serializers import ListingSerializer
from ..users.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    """сериализатор для создания  бронирования"""
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())
    # listing = ListingSerializer(read_only=True)
    tenant = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'tenant',
            'listing',
            'check_in',
            'check_out',
            'status',
            'cancel_deadline',
            'created_at',

        ]
        read_only_fields = ['id', 'created_at', 'status']


class BookingCancelSerializer(serializers.ModelSerializer):
    """сериализатор для отмены бронирования"""
    class Meta:
        model = Booking
        fields = ['id']  #  оставляем  id

    def validate(self, attrs):
        booking = self.instance
        if booking.status != 'confirmed':
            raise serializers.ValidationError("Можно отменить только подтверждённое бронирование.")
        return attrs

    def save(self, **kwargs):
        booking = self.instance
        booking.cancel()  # просто вызываем метод cancel(), логика отмены  реализована в модели
        return booking


class BookingActionSerializer(serializers.ModelSerializer):
    """подтверждения/отклонения бронирования арендодателем"""

    action = serializers.ChoiceField(choices=['confirm', 'reject'])

    class Meta:
        model = Booking
        fields = ['id', 'action']

    def save(self, **kwargs):
        booking = self.instance
        action = self.validated_data['action']

        if action == 'confirm':
            booking.confirm()
        elif action == 'reject':
            booking.reject()
        return booking
