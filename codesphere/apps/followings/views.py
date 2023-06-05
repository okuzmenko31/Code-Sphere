from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.followings.utils import FollowingMixin


class FollowAPIView(FollowingMixin,
                    APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_request(self) -> WSGIRequest:
        return self.request

    def post(self, *args, **kwargs):
        following_category, error = self.get_following_category(self.kwargs['category_id'])
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        following_object, error = self.get_following_object(following_category,
                                                            self.kwargs['following_id'])
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        msg = self.follow(following_object).msg
        return Response({'info': msg})
