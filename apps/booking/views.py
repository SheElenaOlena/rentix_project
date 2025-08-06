from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Booking
from .serializers import (BookingSerializer,
                         BookingCancelSerializer,
                         BookingActionSerializer)



class BookingCreateView(APIView):
    """Создание бронирования"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # или tenant=request.user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingCancelView(APIView):
    """Отмена бронирования пользователем"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk, tenant=request.user)
        serializer = BookingCancelSerializer(instance=booking)
        serializer.save()
        return Response({'detail': 'Бронирование отменено'}, status=status.HTTP_200_OK)


class BookingActionView(APIView):
    """
    Представление для подтверждения или отклонения бронирования арендодателем.
    """
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)

        # Проверка: только владелец объявления может управлять бронированием
        if booking.listing.owner != request.user:
            raise PermissionDenied("Вы не можете управлять этим бронированием.")

        serializer = BookingActionSerializer(instance=booking, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': f'Бронирование {serializer.validated_data["action"]}.'},
                                            status=status.HTTP_200_OK)



class FilteredBookingsView(generics.ListAPIView):
    """Просмотр бронирований текущего пользователя с фильтрацией по статусу"""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        queryset = Booking.objects.filter(tenant=self.request.user)
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset
