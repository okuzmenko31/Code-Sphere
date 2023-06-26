from rest_framework import generics, authentication
from apps.global_permissions import IsOwnerOrReadOnly
from .serializers import CommentsSerializer
from .models import Comments
from apps.content_type_instances.views import ContentTypeInstanceCreateAPIView


class CommentsListCreateAPIView(ContentTypeInstanceCreateAPIView):
    model = Comments
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_url_kwarg = 'comment_id'
