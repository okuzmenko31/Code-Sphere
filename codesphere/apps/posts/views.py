from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     ListAPIView)
from .serializers import PostsSerializer, UnconfirmedPostsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Posts
from apps.global_permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from apps.notifications.utils import NotificationsMixin
from .utils import ViewsMixin, get_user_liked_posts, get_best_posts


class PostsAPIView(NotificationsMixin,
                   ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(is_confirmed=True).prefetch_related('tags')

    def perform_create(self, serializer):
        serializer.save(is_confirmed=False,
                        creator=self.request.user)


class PostDetailAPIView(ViewsMixin,
                        RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]
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


class LikedPostsListAPIView(ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return get_user_liked_posts(self.request.user)


class BestPostsListAPIView(ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    def get_queryset(self):
        return get_best_posts()
