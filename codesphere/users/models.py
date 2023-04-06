from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .services import get_clean_email


class UserManager(BaseUserManager):
    def generate_username(self, email):
        """
        Generates unique username based on 'email' field.
        """

        if not email:
            raise ValueError('Email must be provided')
        username = '@' + get_clean_email(email).lower()
        if not self.filter(username=username).exists():
            return username
        suffix = 2
        while self.filter(username=username + str(suffix)).exists():
            suffix += 1
        return username + str(suffix)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
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


class User(AbstractBaseUser, PermissionsMixin):
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

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                related_name='profile',
                                )
    avatar = models.ImageField(upload_to='images/user',
                               verbose_name='Avatar',
                               blank=True)
    bio = models.TextField(max_length=700, verbose_name='Bio', blank=True)
    country = models.CharField(max_length=150,
                               verbose_name='Country',
                               blank=True)
    city = models.CharField(max_length=170,
                            verbose_name='City',
                            blank=True)
    twitter = models.URLField(max_length=450,
                              verbose_name='Twitter link',
                              blank=True)
    facebook = models.URLField(max_length=450,
                               verbose_name='Facebook link',
                               blank=True)
    github = models.URLField(max_length=450,
                             verbose_name='GitHub link',
                             blank=True)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.user} profile'


class Token(models.Model):
    TOKEN_TYPES = (
        ('su', 'Sign Up Token'),
        ('ce', 'Change Email Token'),
        ('pr', 'Password Reset Token')
    )
    token = models.CharField(max_length=32,
                             verbose_name='Token',
                             unique=True,
                             blank=True)
    token_type = models.CharField(max_length=2,
                                  verbose_name='Type of token',
                                  choices=TOKEN_TYPES,
                                  blank=True,
                                  null=True)
    owner_email = models.EmailField(unique=True,
                                    verbose_name='Owner of token',
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
