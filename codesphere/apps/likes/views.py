from rest_framework.response import Response
from rest_framework import generics, authentication
from .models import Likes

from .serializers import LikesSerializer
from apps.content_type_instances.views import ContentTypeInstanceCreateAPIView
from apps.global_permissions import IsOwnerOrReadOnly
from .utils import check_exist_like


class LikesListCreateAPIView(ContentTypeInstanceCreateAPIView):
    model = Likes
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer

    def create(self, request, *args, **kwargs):
        if check_exist_like(instance_type=self.kwargs['instance_value'],
                            user=self.request.user,
                            instance_id=self.kwargs['instance_id']):
            return Response({'success': 'You successfully removed your like!'})
        response = super().create(request, *args, **kwargs)
        return response


class LikeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_url_kwarg = 'like_id'
