from rest_framework import generics, permissions, authentication, status
from rest_framework.response import Response
from apps.global_permissions import IsOwnerOrReadOnly
from .serializers import CommentsSerializer
from .models import Comments
from .utils import CommentsMixin


class CommentsCreateAPIView(CommentsMixin,
                            generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        return self.comments_by_instance_type(instance_type=self.kwargs['instance_value'],
                                              instance_id=self.kwargs['instance_id'])

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        error = self.check_kwargs(instance_value=self.kwargs['instance_value'],
                                  instance_id=self.kwargs['instance_id'])
        if error is not None:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        return response

    def perform_create(self, serializer):
        instance, error = self.get_instance_by_id(instance_type=self.kwargs['instance_value'],
                                                  instance_id=self.kwargs['instance_id'])
        if instance is not None:
            serializer.save(content_object=instance,
                            creator=self.request.user,
                            instance_type=self.kwargs['instance_value'])

    def create(self, request, *args, **kwargs):
        error = self.check_kwargs(instance_value=self.kwargs['instance_value'],
                                  instance_id=self.kwargs['instance_id'])
        if error is not None:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        response = super().create(request, *args, **kwargs)
        return response


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_url_kwarg = 'comment_id'
