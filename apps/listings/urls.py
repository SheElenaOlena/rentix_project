from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.listings.views import PopularListingsView, MostReviewedListingsView
from .views import ModelViewSet, ListingViewSet, LocationViewSet, ListingRetrieveView

router = DefaultRouter()
router.register('listings', ListingViewSet)
router.register(r'locations', LocationViewSet)
# urlpatterns = router.urls

urlpatterns = [
    path('listings/popular/', PopularListingsView.as_view(), name='popular-listings'),
    path('listings/reviewed/', MostReviewedListingsView.as_view(), name='most-reviewed-listings'),
    path('listings/<int:pk>/', ListingRetrieveView.as_view(), name='listing-detail'),

]

urlpatterns += router.urls