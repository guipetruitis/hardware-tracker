from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, StoreViewSet, HardwareViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'hardware', HardwareViewSet, basename='hardware')

urlpatterns = router.urls
