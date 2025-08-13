from django.db import models
from django.contrib import admin
from apps.users.models import User
from apps.listings.models import Listing





"""История просмотров"""
class ViewHistory(models.Model):
    """сохранять запросы и просмотры от анонимных гостей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        """убираем дубликатов в запросах"""
        unique_together = ('user', 'listing')


    def __str__(self):
        return f"{self.user} viewed {self.listing.title} at {self.viewed_at}"

"""История поисковых запросов"""
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    keyword = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']

    def __str__(self):
        return f"{self.user} viewed '{self.keyword}'"

"""Популярные запросы по ключевым словам"""
class KeywordSearch(models.Model):
    keyword = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('keyword',)
