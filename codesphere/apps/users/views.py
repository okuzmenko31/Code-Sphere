from django.contrib.auth import authenticate
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status, mixins, viewsets
from .serializers import (RegistrationSerializer,
                          LoginSerializer,
                          ChangeEmailSerializer,
                          SendPasswordResetMailSerializer,
                          PasswordResetSerializer,
                          UserProfileSerializer)
from .permissions import IsNotAuthenticated, IsOwnerOrReadOnly
from rest_framework.views import APIView
from .models import User, AuthToken, UserProfile
from .token import TokenTypes, AuthTokenMixin, get_token_data
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication
from .utils import create_user_profile


class UserRegistrationAPIView(AuthTokenMixin,
                              generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsNotAuthenticated]
    token_type = TokenTypes.SIGNUP
    html_message_template = 'users/confirm_email_message.html'
    mail_with_celery = False

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        tokenized_mail_message = self.send_tokenized_mail(
            self.request.data['email'])

        return Response({
            'status': 200,
            'message': tokenized_mail_message,
            'data': response.data
        }, status=status.HTTP_200_OK)


class ConfirmEmailAPIView(AuthTokenMixin,
                          APIView):
    permission_classes = [IsNotAuthenticated]
    token_type = TokenTypes.SIGNUP

    def get(self, *args, **kwargs):
        token = self.kwargs.pop('token')
        email = self.kwargs.pop('email')
        token_data = get_token_data(token, email)
        if token_data.token:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            token_data.token.delete()
            create_user_profile(user)
            return Response({'success': 'You successfully registered and confirmed your email!'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': token_data.error}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [IsNotAuthenticated]

    def get(self, *args, **kwargs):
        data = {
            'user': str(self.request.user),
            'auth': str(self.request.auth)
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = self.request.data['email']
        password = self.request.data['password']
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            data = {
                'message': 'Successful authentication',
                'token': user.auth_token.key
                # we can call user.auth_token because in Token model
                # have related_name="auth_token" to user instance.
                # you can check it here 'rest_framework.authtoken.models'.
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Provided email or password is wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, *args, **kwargs):
        user = self.request.user
        user.auth_token.delete()
        user_tokens = AuthToken.objects.filter(
            token_owner=user.email, expired=False)
        for token in user_tokens:
            token.delete()
        try:
            logout(self.request)
        except User.DoesNotExist:
            return Response({'error': 'Logout error'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'You successfully logged out!'}, status=status.HTTP_200_OK)


class ChangeEmailAPIView(AuthTokenMixin,
                         APIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    token_type = TokenTypes.CHANGE_EMAIL
    html_message_template = 'users/confirm_email_changing.html'
    mail_with_celery = True

    def post(self, *args, **kwargs):
        serializer = ChangeEmailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = self.request.data['email']
        tokenized_mail_message = self.send_tokenized_mail(email)
        return Response({'success': tokenized_mail_message}, status=status.HTTP_200_OK)


class ChangeEmailConfirmAPIView(AuthTokenMixin,
                                APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    token_type = TokenTypes.CHANGE_EMAIL

    def get(self, *args, **kwargs):
        token = kwargs.pop('token')
        new_email = kwargs.pop('email')
        token_data = get_token_data(token, new_email)
        if token_data.token:
            user = self.request.user
            user.email = new_email
            user.save()
            token_data.token.delete()
            return Response({'success': 'You successfully changed your email'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': token_data.error}, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetAPIView(AuthTokenMixin,
                               APIView):
    serializer_class = SendPasswordResetMailSerializer
    token_type = TokenTypes.PASSWORD_RESET
    html_message_template = 'users/password_reset_msg.html'
    mail_with_celery = False

    def post(self, *args, **kwargs):
        serializer = SendPasswordResetMailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = self.request.data['email']
        tokenized_mail_message = self.send_tokenized_mail(email)
        return Response({'success': tokenized_mail_message},
                        status=status.HTTP_200_OK)


class PasswordResetAPIView(AuthTokenMixin,
                           APIView):
    serializer_class = PasswordResetSerializer
    token_type = TokenTypes.PASSWORD_RESET

    def get(self, *args, **kwargs):
        token = self.kwargs.pop('token')
        email = self.kwargs.pop('email')
        token_data = get_token_data(token, email)
        if token_data.token:
            return Response({'message': 'Password reset page. Write new password.'},
                            status=status.HTTP_200_OK)
        else:
            self.serializer_class = None
            return Response({'error': token_data.error},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, *args, **kwargs):
        token = self.kwargs.pop('token')
        email = self.kwargs.pop('email')
        token_data = get_token_data(token, email)
        if token_data.token:
            serializer = PasswordResetSerializer(data=self.request.data,
                                                 context={'email': kwargs['email']})
            serializer.is_valid(raise_exception=True)
            token_data.token.delete()
            return Response({'success': 'Password reset success.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': token_data.error},
                            status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'slug'
    lookup_url_kwarg = 'user_slug'

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if not self.request.user.is_authenticated or self.get_object().user.id != self.request.user.id:
            del response.data['settings']
        return response


class UserProfileForUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    APIView which returns user's profile if
    user is authenticated. User can access to
    his profile without ulr kwargs and with url
    'api/v1/users/profile/'.
    """
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    lookup_field = None

    def get_object(self):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        return profile
