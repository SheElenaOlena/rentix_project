from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.listings.choices.property_types import PROPERTY_TYPES
from apps.listings.choices.roles import Role
from apps.listings.filters import ListingFilter
from apps.listings.models import Listing, Location
from apps.listings.serializers import ListingSerializer, LocationSerializer
from apps.users.permissions import IsLandlordOwnerOrReadOnly, IsTenant


class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.filter(is_active=True)
    # queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsLandlordOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    filterset_class = ListingFilter
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Показываем только объявления текущего пользователя
        return self.queryset.filter(owner=self.request.user)

    """вызывается после проверки данныхlistings_location
      передать текущего пользователя (request.user) как владельца объявления.
      """
    def perform_create(self, serializer):
        # Сохраняем объявление с текущим пользователем как владельцем
        serializer.save(owner=self.request.user)

        # Меняем роль пользователя, если он был Tenant
        user = self.request.user

        if user.role == Role.TENANT:
            user.role = Role.LANDLORD
            user.save()
            print("Роль изменена:", user.role)  # ← Проверка в консоли


class ListingUpdateView(UpdateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsLandlordOwnerOrReadOnly]

    def get_queryset(self):
        # Только свои объявления!
        # Возвращаем объявления, принадлежащие текущему пользователю (арендодателю)
        # Это ограничивает редактирование только своими объектами
        return self.queryset.filter(owner=self.request.user)


class PropertyTypeChoicesView(APIView):
    def get(self, request):
        return Response([
            {"value": choice.name, "label": choice.value}
            for choice in PROPERTY_TYPES
        ])

class ListingListView(generics.ListAPIView):
    queryset = Listing.objects.filter(is_active=True)
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsTenant]


# views.py
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
