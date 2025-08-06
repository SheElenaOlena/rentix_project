from rest_framework.routers import DefaultRouter
from .views import ModelViewSet, ListingViewSet, LocationViewSet

router = DefaultRouter()
router.register('listings', ListingViewSet)
router.register(r'locations', LocationViewSet)
urlpatterns = router.urls