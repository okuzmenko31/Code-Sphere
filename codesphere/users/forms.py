from django import forms
from django.contrib.auth.forms import UserCreationForm
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
                                                                  'placeholder': 'Password'})),
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Password confirmation'}))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'class': 'form-control',
                                                 'placeholder': 'Password'}

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        self.validate_password(password1)
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password mismatch')
        return password2
