from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     ListAPIView)
from .serializers import PostsSerializer, UnconfirmedPostsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Posts
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


class PostsAPIView(ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(is_confirmed=True).prefetch_related('tags')

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(is_confirmed=False)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_url_kwarg = 'post_id'


class UnconfirmedPostsAPIView(ListAPIView):
    """
    APIView which is available only for admins and
    returns only unconfirmed posts.
    """
    queryset = Posts.objects.all()
    serializer_class = UnconfirmedPostsSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return self.queryset.filter(is_confirmed=False).prefetch_related('tags')


class UnconfirmedPostsDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = UnconfirmedPostsSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    lookup_url_kwarg = 'post_id'
