from rest_framework import serializers
from apps.listings.choices.property_types import PROPERTY_TYPES
from apps.listings.models import Listing, Location
from django.contrib.auth.models import Group
from django.db import transaction



# 🏙️ Сериализатор для связанной модели Location
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['city', 'street', 'house_number', 'country', 'postal_code']  # Поля, которые будут сериализованы


# 📋 Сериализатор для основной модели Listing
class ListingSerializer(serializers.ModelSerializer):
    # Вложенный сериализатор для связи с Location (OneToOne / ForeignKey)
    location = LocationSerializer()
    property_type = serializers.ChoiceField(choices=PROPERTY_TYPES.choices())
    average_rating = serializers.SerializerMethodField()


    class Meta:
        model = Listing
        # Исключаем поля, которые не должны приходить от клиента или обрабатываются вручную
        # exclude = ['owner', 'views_count', 'created_at', 'updated_at']
        fields = '__all__'
        read_only_fields = ['owner', 'views_count', 'created_at', 'updated_at']

    def get_average_rating(self, obj):
        return round(obj.average_rating(), 1)



    # 🎯 Метод для создания нового объекта Listing
    def create(self, validated_data):
        # Отделяем данные по локации от общих данных
        location_data = validated_data.pop('location', None)
        # Получаем текущего пользователя из контекста сериализатора
        user = self.context['request'].user

        if not location_data:
            raise serializers.ValidationError({'location': 'Поле "location" обязательно для создания объявления.'})

        with transaction.atomic():
            # Создаём объект Location (связь один-к-одному или внешний ключ)
            location = Location.objects.create(**location_data)
            validated_data.pop('owner', None)  # 💡 Удаляем owner, если он есть, иначе ошибка 500
            # Создаём новое объявление и связываем с локацией и владельцем
            listing = Listing.objects.create(location=location, owner=user, **validated_data)

            # 🔁 Если пользователь был в группе Tenant — переводим в Landlord
            if user.groups.filter(name='Tenant').exists():
                tenant_group = Group.objects.get(name='Tenant')
                landlord_group = Group.objects.get(name='Landlord')
                user.groups.remove(tenant_group)
                user.groups.add(landlord_group)

        return listing

    # 🔄 Метод для обновления существующего объекта Listing и связанной локации
    def update(self, instance, validated_data):
        # Попытка получить вложенные данные локации (если они были отправлены)
        location_data = validated_data.pop('location', None)
        if not isinstance(location_data, dict):
            raise serializers.ValidationError({'location': 'Некорректные данные локации — ожидается словарь.'})

        if location_data:
            # Получаем связанную локацию и обновляем её поля
            location_instance = instance.location
            for attr, value in location_data.items():
                setattr(location_instance, attr, value)
            location_instance.save()

        # Обновляем остальные поля модели Listing
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



"""
 📌 LocationSerializer: отдельный сериализатор для адреса, встроенный в ListingSerializer.
    🔨 create(): создаёт новую локацию и объявление, связывает с текущим пользователем, переключает группы.
    🔁 update(): обновляет как поля самого объявления, так и вложенную модель Location.
"""