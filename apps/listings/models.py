from django.db import models
from .choices.property_types import PROPERTY_TYPES
from apps.users.models import User
from django.contrib import admin
from django.db.models import Avg





class Location(models.Model):
    """Адрес объекта"""
    city = models.CharField(
        max_length=100,
        verbose_name='Город',
        help_text='Название города (например: Берлин)'
    )
    street = models.CharField(
        max_length=100,
        verbose_name='Улица',
        help_text='Название улицы (например: Friedrichstraße)'
    )
    house_number = models.CharField(
        max_length=20,
        verbose_name='Номер дома',
        help_text='Номер здания (например: 12A)'
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Почтовый индекс'
    )
    country = models.CharField(
        max_length=100,
        default='Germany',
        verbose_name='Страна'
    )

    class Meta:
        """Задали UniqueConstraint, чтобы избежать дублей: один и тот же адрес не должен повторяться"""
        constraints = [
            models.UniqueConstraint(
                fields=['city', 'street', 'house_number'],
                name='unique_location_address'
            )
        ]
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f"{self.city}, {self.street} {self.house_number}"


class Listing(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Местоположение'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    rooms = models.PositiveIntegerField(
        verbose_name='Количество комнат'
    )
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES.choices(),
        default=PROPERTY_TYPES.apartment.name,
        verbose_name='Тип жилья'
    )
    views_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )
    # 👇 СВЯЗЬ: арендодатель, который разместил объект
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='listings'
    )

    def average_rating(self):
        return self.reviews.filter(is_published=True).aggregate(avg=Avg('rating'))['avg'] or 0

    def is_available(self, start_date, end_date):
        """проверка на доступность объекта, на выбраные даты,
          и активность объекта
        """
        if not self.is_active:
            return False

        return not self.bookings.filter(
            status='confirmed',
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'location'],
                name='unique_listing_title_location'
            )
        ]
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title
