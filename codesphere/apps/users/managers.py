from django.contrib.auth.base_user import BaseUserManager
from .services import clean_email
from django.utils import timezone


class UserManager(BaseUserManager):

    def generate_username(self, email: str) -> str:
        """
        Generates username for user
        based on provided email.

        :param email: provided email.
        :return: generated username.
        """
        if not email:
            raise ValueError('Email must be provided!')
        username = '@' + clean_email(email)
        if not self.filter(username=username).exists():
            return username
        suffix = 1
        while self.filter(username=username + str(suffix)).exists():
            suffix += 1
        return username + str(suffix)

    def _create_user(self, email, password, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        username = extra_fields.get('username')
        if not username or self.filter(username=username).exists():
            extra_fields['username'] = self._generate_username(email)
        user = self.model(email=email,
                          is_active=True,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self._create_user(email, password, **extra_fields)
        user.is_admin = True
        user.save(using=self.db)
        return user
