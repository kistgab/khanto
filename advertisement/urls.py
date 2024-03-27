from advertisement.views import AdvertisementViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", AdvertisementViewSet)
urlpatterns = router.urls
