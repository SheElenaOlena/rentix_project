from rest_framework import  status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.listings.models import Listing
from django.core.exceptions import PermissionDenied
from apps.booking.models import Booking
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer
from rest_framework import filters



class ReviewCreateView(APIView):
    """Создание отзыва"""

    permission_classes = [IsAuthenticated]

    def post(self, request, listing_id):
        listing = get_object_or_404(Listing, pk=listing_id)

        # Проверка, что пользователь бронировал это объявление
        has_booking = Booking.objects.filter(
            tenant=request.user,
            listing=listing,
            status='confirmed'  # проверка, что статус соответствует завершённому проживанию
        ).exists()

        if not has_booking:
            raise PermissionDenied("Вы можете оставить отзыв только после проживания.")

        # Проверка: не оставлял ли пользователь уже отзыв
        if listing.reviews.filter(author=request.user).exists():
            return Response(
                {"detail": "Вы уже оставили отзыв для этого объявления."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, listing=listing)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListingReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        listing_id = self.kwargs['listing_id']
        return Review.objects.filter(listing_id=listing_id).order_by('-created_at')


