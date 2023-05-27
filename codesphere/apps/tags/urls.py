from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagsListAPIView, TagDetailAPIView

# router = DefaultRouter()
# router.register(r'', viewset=TagsViewSet, basename='tags')

urlpatterns = [
    path('', TagsListAPIView.as_view(), name='tags_list'),
    path('<slug:slug>/', TagDetailAPIView.as_view(), name='tag_detail')
]
