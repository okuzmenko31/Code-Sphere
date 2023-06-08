from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     ListAPIView)
from .serializers import PostsSerializer, UnconfirmedPostsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Posts
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .utils import PostMixin
from apps.notifications.utils import NotificationsMixin


class PostsAPIView(PostMixin,
                   NotificationsMixin,
                   ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(is_confirmed=True).prefetch_related('tags')

    def perform_create(self, serializer):
        post = serializer.save(is_confirmed=False,
                               creator=self.request.user)
        message = self.get_post_notification_message(post)
        self.notification_message = message
        creator_followers = self.get_post_creator_followers(post)
        self.send_mass_notifications(sender=post.creator,
                                     recipients=creator_followers)


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
