from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import User


class CustomSocialAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super(CustomSocialAdapter, self).populate_user(request, sociallogin, data)
        if 'first_name' and 'last_name' in data:
            user.full_name = f'{data["first_name"]} {data["last_name"]}'
        elif 'full_name' in data:
            user.full_name = data['full_name']
        elif 'name' in data:
            user.full_name = data['name']
        else:
            user.full_name = 'CodeSphere User'
        if 'username' in data:
            user.username = '@' + data['username']
        else:
            user.username = User.objects.generate_username(data['email'])
        return user
