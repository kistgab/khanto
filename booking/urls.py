from booking.views import BookingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", BookingViewSet)
urlpatterns = router.urls
