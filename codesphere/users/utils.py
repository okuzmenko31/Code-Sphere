from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Token


class CreateConfirmationTokenMixin:
    __token = None
    __token_owner = None
    token_type = None

    @staticmethod
    def token_types():
        token_types = []
        for item in Token.TOKEN_TYPES:
            token_types.append(item[0])
        return token_types

    def check_token_type(self):
        if self.token_type in self.token_types():
            return True
        else:
            return False

    def create_token(self):
        if self.check_token_type():
            if Token.objects.filter(token_type=self.token_type, owner_email=self.__token_owner).exists():
                Token.objects.get(token_type=self.token_type, owner_email=self.__token_owner).delete()
                self.__token = Token.objects.create(token_type=self.token_type,
                                                    owner_email=self.__token_owner)
            else:
                self.__token = Token.objects.create(token_type=self.token_type,
                                                    owner_email=self.__token_owner)
        return self.__token

    @property
    def token_owner(self):
        return self.__token_owner

    @token_owner.setter
    def token_owner(self, email):
        self.__token_owner = email
        self.create_token()

    def get_token(self):
        return self.__token


class CreateMailContextMixin:
    __subject = None
    __message = ''
    __success_message = None

    @classmethod
    def _set_subject(cls, token_type):
        if token_type == 'su':
            cls.__subject = 'CodeSphere - complete registration.'
        elif token_type == 'ce':
            cls.__subject = 'CodeSphere - complete changing email'
        else:
            cls.__subject = 'CodeSphere - complete password reset'

    @classmethod
    def _set_success_message(cls, token_type):
        if token_type == 'su':
            cls.__success_message = 'Mail with registration link has ' \
                                    'been sent to your email.'
        elif token_type == 'ce':
            cls.__success_message = 'Mail with email changing ' \
                                    'confirmation has been sent to your new email.\n' \
                                    'Your email in this account will be changed' \
                                    'after confirmation.'
        else:
            cls.__success_message = 'Mail with password reset confirmation has been sent ' \
                                    'to your email.'

    def get_context(self, token_type):
        self._set_subject(token_type)
        self._set_success_message(token_type)

        context = {
            'subject': self.__subject,
            'message': self.__message,
            'success_message': self.__success_message
        }
        return context


class ConfirmationMailMixin(CreateMailContextMixin):
    mail_with_celery = False
    html_message_template = None

    def send_confirmation_mail(self, request, email, token_type, token):
        mail_context = self.get_context(token_type)
        cont = {
            'email': str(email),
            'domain': '127.0.0.1:8000',
            'site_name': 'CodeSphere',
            'token': urlsafe_base64_encode(force_bytes(token.token)),
            'protocol': 'https' if request.is_secure() else 'http'
        }
        subject = mail_context['subject']
        message = mail_context['message']
        html_msg = render_to_string(self.html_message_template, cont)

        if self.mail_with_celery:
            pass
        else:
            send_mail(subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      [email],
                      html_message=html_msg)

    def get_success_message(self, token_type):
        context = self.get_context(token_type)
        success_message = context['success_message']
        return success_message
