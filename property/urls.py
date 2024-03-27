from property.views import PropertyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", PropertyViewSet)
urlpatterns = router.urls
