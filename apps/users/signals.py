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