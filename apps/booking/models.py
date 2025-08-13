from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib import admin
from apps.users.models import User
from apps.listings.models import Listing
from apps.listings.choices.booking_statuses import BookingStatus
from django.utils import timezone
from datetime import timedelta






class Booking(models.Model):
    tenant = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='bookings'
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE,
        related_name='bookings'
    )
    check_in = models.DateField()
    check_out = models.DateField()
    cancel_deadline = models.DateField(null=True, blank=True)   #  "отмена до определённой даты"

    status = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.name) for tag in BookingStatus],
        default=BookingStatus.PENDING.value,
    )

    @property
    def is_confirmed(self):
        return self.status == BookingStatus.CONFIRMED.value

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f"{self.tenant.email} → {self.listing.title} [{self.check_in}–{self.check_out}]"

    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError('Дата выезда должна быть позже даты заезда.')

        if not self.listing.is_active:
            raise ValidationError('Объект не активен — бронирование невозможно.')

        overlapping = Booking.objects.filter(
            listing=self.listing,
            status=BookingStatus.CONFIRMED,
            check_in__lt=self.check_out,
            check_out__gt=self.check_in
        ).exclude(pk=self.pk)

        if overlapping.exists():
            raise ValidationError('Выбранные даты уже заняты другим бронированием.')

    # 🔄 Отмена бронирования арендатором
    def cancel(self):
        if not self.is_confirmed:
            raise ValidationError("Можно отменить только подтверждённое бронирование.")

        if self.cancel_deadline and timezone.now().date() > self.cancel_deadline:
            raise ValidationError("Срок отмены истёк.")

        self.status = BookingStatus.CANCELLED.value
        self.save()

    def save(self, *args, **kwargs):
        if not self.cancel_deadline and self.check_in:
            self.cancel_deadline = self.check_in - timedelta(days=2)
        self.full_clean()
        super().save(*args, **kwargs)


    # ✅ Подтвердить бронирование
    def confirm(self) -> None:
        if self.status != BookingStatus.PENDING.value:  #статус бронирования — PENDING
            raise ValidationError('Только PENDING бронирование можно подтвердить.')

        self.status = BookingStatus.CONFIRMED.value   #Обновляет статус на CONFIRMED
        self.save()                             #Сохраняет изменения в базе

    # ❌ Отклонить бронирование
    def reject(self):
        if self.status != BookingStatus.PENDING.value:
            raise ValidationError('Только PENDING бронирование можно подтвердить.')

        self.status = BookingStatus.REJECTED.value
        self.save()



