from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from .models import User


class CustomSocialAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super(CustomSocialAdapter, self).populate_user(request, sociallogin, data)
        if data['first_name'] and data['last_name']:
            user.full_name = f'{data["first_name"]} {data["last_name"]}'
        elif data['full_name']:
            user.full_name = data['full_name']
        elif data['name']:
            user.full_name = data['name']
        else:
            user.full_name = 'CodeSphere User'
        user.username = User.objects.generate_username(data['email'])
        return user
