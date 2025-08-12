from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.listings.views import PopularListingsView, MostReviewedListingsView, ListingListView
from .views import ModelViewSet, ListingViewSet, LocationViewSet, ListingRetrieveView

router = DefaultRouter()
router.register('listings', ListingViewSet)
router.register(r'locations', LocationViewSet)
urlpatterns = router.urls

# urlpatterns = [
#
#     path('listings/popular/', PopularListingsView.as_view(), name='popular-listings'),   # популярные
#     path('listings/reviewed/', MostReviewedListingsView.as_view(), name='most-reviewed-listings'),   # самые обсуждаемые
#      path('listings/<int:pk>/', ListingRetrieveView.as_view(), name='listing-detail'),  # конкретное объявление
#      path('', ListingListView.as_view(), name='home-listings')
# ]
#
# urlpatterns += router.urls