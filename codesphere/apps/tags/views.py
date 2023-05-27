from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .models import Tags
from .serializers import TagsSerializer
from .permissions import IsAdminOrReadOnly


class TagsViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  GenericViewSet):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    # def get_queryset(self):
    #     try:
    #         return self.queryset.prefetch_related('followers')
    #     except (Exception,):
    #         return super().get_queryset()
