from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .validators import CustomPasswordValidation
from .models import User


class SignUpEmailForm(forms.Form):
    email = forms.EmailField(label='',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email',
                                                           'autocomplete': 'off'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            msg = 'User with this email is already registered'
            raise forms.ValidationError(msg)
        return email


class SignUpForm(CustomPasswordValidation, UserCreationForm):
    email = forms.EmailField(label='E-mail',
                             required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'E-mail'}))
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Password'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Password confirmation'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Password mismatch')
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        self.validate_password(password1)
        return password1


class SignInForm(forms.Form):
    email = forms.EmailField(label='',
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'autocomplete': 'email',
                                                            'placeholder': 'E-mail'}))
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'autocomplete': 'password',
                                                                 'placeholder': 'Password'}))

    def clean(self):
        data = self.cleaned_data
        try:
            email = data['email']
        except (Exception,):
            raise forms.ValidationError('Write your email in format like this: example@example.com')
        password = data['password']

        try:
            user = User.objects.get(email=email)
        except (Exception,):
            raise forms.ValidationError('User with this email does not exits!')
        if not user.check_password(password):
            raise forms.ValidationError('The password is wrong!')
        return data
