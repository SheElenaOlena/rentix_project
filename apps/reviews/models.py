from django.db import models
from django.db.models import F
from rest_framework.response import Response
from apps.listings.models import Listing
from apps.users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin




# 1. Модель отзыва (Review)
class Review(models.Model):
     author = models.ForeignKey(User, on_delete=models.CASCADE)     #ссылка на пользователя (арендатор)
     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')    # ссылка на объявление
     rating = models.PositiveSmallIntegerField(
         validators=[MinValueValidator(1), MaxValueValidator(5)]
     )     #оценка  от 1 до 5
     comment = models.TextField()     #текст отзыва
     created_at = models.DateTimeField(auto_now_add=True)   # дата публикации
     updated_at = models.DateTimeField(auto_now=True)
     is_published = models.BooleanField(default=True)  # для модерации

     class Meta:
          unique_together = ('author', 'listing')  # один отзыв на одно объявление

     def __str__(self):
          return f"⭐ {self.rating} by {self.author} → {self.listing.title}"


     """ 2. Обновляем счетчик при каждом просмотре: 
          В RetrieveAPIView для объявления добавить логику увеличения счётчика:
     """


     def retrieve(self, request, *args, **kwargs):
         instance = self.get_object()
         instance.views_count = F('views_count') + 1
         instance.save(update_fields=['views_count'])
         instance.refresh_from_db()
         serializer = self.get_serializer(instance)
         return Response(serializer.data)









