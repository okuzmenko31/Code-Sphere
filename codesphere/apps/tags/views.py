from rest_framework import generics
from .models import Tags
from .serializers import TagsSerializer
from .permissions import IsAdminOrReadOnly


class TagsListAPIView(generics.ListCreateAPIView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
