from rest_framework import generics, permissions, authentication, status
from rest_framework.response import Response

from .serializers import CommentsSerializer
from .models import Comments
from .utils import CommentsMixin


class CommentsListAPIView(CommentsMixin,
                          generics.ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class CommentsCreateAPIView(CommentsMixin,
                            generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        instance, error = self.get_instance_by_id(instance_type=self.kwargs['instance_value'],
                                                  instance_id=self.kwargs['instance_id'])
        if instance is not None:
            serializer.save(content_object=instance, user=self.request.user)

    def create(self, request, *args, **kwargs):
        error = self.check_kwargs(instance_value=self.kwargs['instance_value'],
                                  instance_id=self.kwargs['instance_id'])
        if error is not None:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        response = super().create(request, *args, **kwargs)
        return response
