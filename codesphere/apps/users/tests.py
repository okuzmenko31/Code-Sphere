from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from .models import User, AuthToken
from .token import AuthTokenMixin, get_token_data, TokenData, MESSAGES


class UserTokenTests(TestCase):

    def test_create_token(self):
        mixin = AuthTokenMixin()
        mixin.token_type = 'su'
        email = 'test@example.com'
        token_data = mixin._create_token(email)
        self.assertIsNotNone(token_data.token)
        self.assertIsNone(token_data.error)
        token = AuthToken.objects.get(token_owner=email,
                                      token_type=mixin.token_type)
        self.assertEqual(token_data.token, token)

    def test_send_tokenized_mail(self):
        mixin = AuthTokenMixin()
        mixin.token_type = 'su'
        mixin.html_message_template = 'users/confirm_email_message.html'
        email = 'test@example.com'
        response = mixin.send_tokenized_mail(email)
        success_message = mixin.get_context(token_type=mixin.token_type)['success_message']
        self.assertEqual(response, success_message)

    def test_token_data(self):
        mixin = AuthTokenMixin()
        mixin.token_type = 'su'
        email = 'test@example.com'
        token_data = mixin._create_token(email)
        response = get_token_data(token_data.token.token, email)
        self.assertEqual(response, TokenData(token=token_data.token))
        token_data.token.expired = True
        token_data.token.save()
        response = get_token_data(token_data.token.token, email)
        self.assertEqual(response, TokenData(error=MESSAGES['token_expired_error']))
        token_data.token.delete()
        response = get_token_data(token_data.token.token, email)
        self.assertEqual(response, TokenData(error=MESSAGES['token_miss_error']))


class RegistrationAPITests(APITestCase):

    def test_registration(self):
        url = reverse('registration')
        data = {
            'email': 'test_user@gmail.com',
            'password': 'Test_password1',
            'password1': 'Test_password1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().email, 'test_user@gmail.com')


class LoginLogoutAPITests(APITestCase):

    def setUp(self) -> None:
        user = User.objects.create(email='test_user@gmail.com')
        user.set_password('Test_password1')
        user.save()
        Token.objects.create(user=user)

    def test_get_login(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_login(self):
        url = reverse('login')
        data = {
            'email': 'test_user@gmail.com',
            'password': 'Test_password1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        url = reverse('logout')
        token = Token.objects.get(user__email='test_user@gmail.com')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthAPITests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='test_user@gmail.com')
        self.user.set_password('Test_password1')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_change_email_send(self):
        url = reverse('change_email_send')
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid token')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        data = {
            'email': 'test_email@gmail.com'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_send(self):
        url = reverse('send_password_reset')
        data = {
            'email': self.user.email
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ConfirmationWithTokenTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test_user@gmail.com')
        self.user.set_password('Test_password1')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_email_confirm(self):
        auth_token = AuthToken.objects.create(token_owner=self.user.email, token_type='su')
        url = reverse('confirm-email', kwargs={'token': auth_token,
                                               'email': self.user.email})
        response = self.client.get(url)
        token_data = get_token_data(auth_token, self.user.email)
        if token_data.token:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_email_confirm(self):
        auth_token = AuthToken.objects.create(token_owner=self.user.email, token_type='ce')
        url = reverse('change_email_confirm', kwargs={'token': auth_token,
                                                      'email': self.user.email})
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid token')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        token_data = get_token_data(auth_token, self.user.email)
        if token_data.token:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_password_reset(self):
        auth_token = AuthToken.objects.create(token_owner=self.user.email, token_type='pr')
        url = reverse('password_reset', kwargs={'token': auth_token,
                                                'email': self.user.email})
        response = self.client.get(url)
        token_data = get_token_data(auth_token, self.user.email)
        if token_data.token:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_password_reset(self):
        auth_token = AuthToken.objects.create(token_owner=self.user.email, token_type='pr')
        url = reverse('password_reset', kwargs={'token': auth_token,
                                                'email': self.user.email})
        data = {
            'password': 'Test_password1',
            'password1': 'Test_password1'
        }
        response = self.client.post(url, data, format='json')
        token_data = get_token_data(auth_token, self.user.email)
        if token_data.token:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
