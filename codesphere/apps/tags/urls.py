from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagsViewSet

router = DefaultRouter()
router.register(r'', viewset=TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls))
]
