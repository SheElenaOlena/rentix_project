from django.utils import timezone
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, request
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

    def get_serializer(self, *args, **kwargs):
        return BookingSerializer(*args, **kwargs)

    def post(self, request):
        # 🔐 Проверка роли пользователя
        if hasattr(request.user, 'role') and request.user.role == 'landlord':
            return Response(
                {'detail': 'Арендодатель не может бронировать жильё.'},
                status=status.HTTP_403_FORBIDDEN
            )


        # data = request.data.copy()
        # data['tenant'] = request.user.id  # автоматически подставляем текущего пользователя

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingCancelView(APIView):
    """Отмена бронирования пользователем"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        print(f"Request user ID: {request.user.id}")

        booking = get_object_or_404(Booking, pk=pk, tenant=request.user)
        # booking = get_object_or_404(Booking, pk=pk)
        print(f"Booking status: {booking.status}")

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

        return Response({
            'detail': f'Бронирование успешно {serializer.validated_data["action"]}.',
            'id': booking.id,
            'new_status': booking.status
        }, status=status.HTTP_200_OK)


class FilteredBookingsView(generics.ListAPIView):
    """Просмотр бронирований текущего пользователя с фильтрацией по статусу"""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        status_param = self.request.query_params.get('status')
        queryset = Booking.objects.filter(tenant=self.request.user)

        if status_param == 'active':
            queryset = queryset.filter(check_out__gte=timezone.now().date())
        elif status_param == 'past':
            queryset = queryset.filter(check_out__lt=timezone.now().date())
        elif status_param:
            queryset = queryset.filter(status=status_param)

        return queryset

class BookingDetailView(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]