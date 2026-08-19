"""
Mobile API routing, mounted at /api/v1/ in config/urls.py.
Each app's viewsets get registered here as they're built, e.g.:
    router.register('products', ProductViewSet, basename='product')
"""
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = router.urls