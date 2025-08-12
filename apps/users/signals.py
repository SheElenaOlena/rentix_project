# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group
# from django.db.models.signals import post_migrate, post_save
# from django.dispatch import receiver
#
# User = get_user_model()
#
# # Создание групп после миграций
# @receiver(post_migrate)
# def create_default_groups(sender, **kwargs):
#     default_groups = ['Tenant', 'Landlord', 'Moderator', 'Admin']
#     for group_name in default_groups:
#         Group.objects.get_or_create(name=group_name)
#
# # Назначение группы при создании пользователя
# @receiver(post_save, sender=User)
# def assign_group_on_user_creation(sender, instance, created, **kwargs):
#     if created:
#         role = getattr(instance, 'role', None)
#         group_name = None
#
#         if role == 'landlord':
#             group_name = 'Landlord'
#         elif role == 'tenant':
#             group_name = 'Tenant'
#         elif role == 'moderator':
#             group_name = 'Moderator'
#         elif role == 'admin':
#             group_name = 'Admin'
#
#         if group_name:
#             group = Group.objects.filter(name=group_name).first()
#             if group:
#                 instance.groups.add(group)

# apps/users/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from apps.listings.models import Listing

User = get_user_model()

@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created and instance.role:
        group_name = instance.role.capitalize()  # 'tenant' → 'Tenant'
        group, _ = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)


@receiver(post_delete, sender=Listing)
     # """удаление Location, если она осталась без объявлений"""
def delete_orphan_location(sender, instance, **kwargs):
    location = instance.location
    if not Listing.objects.filter(location=location).exists():
        location.delete()