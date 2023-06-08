from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, UserProfile
from rest_framework.authtoken.models import Token
from apps.followings.utils import count_followers
from django.template.defaultfilters import timesince


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password])
    password1 = serializers.CharField(write_only=True,
                                      required=True,
                                      validators=[validate_password])

    def validate(self, attrs):
        if attrs['password1'] != attrs['password']:
            raise serializers.ValidationError('Password mismatch.')
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                'User with this email is already exists!')
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create(email=email, is_active=False)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)  # creating authentication token
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
            if Token.objects.filter(user=user).exists():
                user.auth_token.delete()
            Token.objects.create(user=user)  # creating authentication token
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError('The password is wrong!')
        except User.DoesNotExist:
            raise serializers.ValidationError('No such user with this email!')
        return attrs


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(label='New E-mail',
                                   write_only=True,
                                   validators=[UniqueValidator(
                                       queryset=User.objects.all())],
                                   required=True)

    def validate(self, attrs):
        email = attrs['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User with this email is already exists')
        return attrs


class SendPasswordResetMailSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'No such user with this email address!')
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password])
    password1 = serializers.CharField(write_only=True,
                                      required=True,
                                      validators=[validate_password])

    def validate(self, attrs):
        password = attrs['password']
        password1 = attrs['password1']
        email = self.context.get('email')

        if password1 != password:
            raise serializers.ValidationError('Password mismatch')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'No such user with this email address')
        if user.check_password(password):
            raise serializers.ValidationError(
                'New password must not be the same as the old one')
        user.set_password(password)
        user.save()
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'date_joined', 'is_active')


class UserProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField(read_only=True)
    followers_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user_username', 'avatar', 'bio',
                  'location', 'socials', 'settings', 'followers_count')

    def get_user_username(self, instance):
        return instance.user.username

    def get_followers_count(self, instance):
        return count_followers(instance)
