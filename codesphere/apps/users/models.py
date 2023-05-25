import os
import binascii
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.text import slugify
from .services import social_media_json, settings_json, get_from_json
from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=254,
                              unique=True,
                              db_index=True,
                              verbose_name='Email',
                              blank=False,
                              null=False)
    username = models.CharField(max_length=250,
                                verbose_name='Username',
                                unique=True,
                                blank=True,
                                null=False)
    full_name = models.CharField(max_length=250,
                                 verbose_name='Full name',
                                 blank=True)
    is_staff = models.BooleanField(verbose_name='Staff status', default=False)
    is_superuser = models.BooleanField(verbose_name='Superuser status', default=False)
    is_active = models.BooleanField(verbose_name='User activated', default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(verbose_name='Last login', null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='Date joined', auto_now_add=True)
    slug = models.SlugField(unique=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    @classmethod
    def slugify_username(cls, username: str) -> str:
        """Returns 'username' for slug."""
        return slugify(username)

    def save(self, *args, **kwargs):
        if self._state.adding and (User.objects.filter(username=self.username).exists()
                                   or not self.username):
            if not self.full_name:
                self.full_name = 'user'
            self.username = User.objects.generate_username(self.email)
        if self._state.adding and not self.slug:
            self.slug = self.slugify_username(self.username)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                related_name='profile')
    avatar = models.ImageField(upload_to='images/user',
                               verbose_name='Avatar',
                               blank=True,
                               null=True)
    bio = models.CharField(max_length=700,
                           verbose_name='Bio',
                           blank=True,
                           null=True)
    location = models.CharField(max_length=200,
                                verbose_name='Location',
                                blank=True,
                                null=True)
    socials = models.JSONField(verbose_name='Social media links',
                               default=social_media_json)
    settings = models.JSONField(verbose_name='Settings',
                                default=settings_json)

    def __str__(self):
        return f'Profile: {self.user.username}'

    def get_socials(self):
        return get_from_json(self.socials)

    def get_settings(self):
        return get_from_json(self.settings)

    @property
    def twitter(self):
        return self.get_socials()['twitter']

    @property
    def github(self):
        return self.get_socials()['github']

    @property
    def facebook(self):
        return self.get_socials()['facebook']

    @property
    def instagram(self):
        return self.get_socials()['instagram']

    @property
    def is_socials(self):
        return any(self.get_socials().values())

    @property
    def theme(self):
        return self.get_settings()['theme']

    @theme.setter
    def theme(self, theme: str):
        settings = self.get_settings()
        settings['theme'] = theme
        self.settings = settings
        self.save()


class AuthToken(models.Model):
    TOKEN_TYPES = (
        ('su', 'SignUp token'),
        ('ce', 'Change email token'),
        ('pr', 'Password reset token')
    )
    token = models.CharField(unique=True,
                             max_length=32,
                             verbose_name='Token',
                             blank=True,
                             null=True)
    token_type = models.CharField(max_length=2, choices=TOKEN_TYPES,
                                  verbose_name='Token type',
                                  blank=True,
                                  null=True)
    token_owner = models.EmailField(verbose_name='Token owner email',
                                    blank=True,
                                    null=True)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Token creation date')
    expired = models.BooleanField(default=False,
                                  verbose_name='Token expired')

    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'Tokens'

    def __str__(self):
        return f'{self.token}, {self.token_type}'

    @classmethod
    def generate_token(cls):
        return binascii.hexlify(os.urandom(16)).decode()

    def save(self, *args, **kwargs):
        if self._state.adding and (not self.token or
                                   AuthToken.objects.filter(token=self.token).exists()):
            self.token = self.generate_token()
        super().save(*args, **kwargs)

    @classmethod
    def get_token_from_str(cls, token_value: str, token_owner: str):
        return cls.objects.get(token=token_value, token_owner=token_owner)
