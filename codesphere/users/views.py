import json
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import SignUpEmailForm, SignUpForm
from django.views import View
from .models import User
from .token import TokenMixin, get_token_data, TokenTypes
from .forms import SignInForm
from django.conf import settings

DEFAULT_AUTH = settings.AUTHENTICATION_BACKENDS[0]


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class SubmitRegistrationEmail(TokenMixin,
                              View):
    html_message_template = 'users/mails/registration_mail.html'
    token_type = TokenTypes.SIGNUP

    def post(self, *args, **kwargs):
        if is_ajax(self.request):
            form = SignUpEmailForm(self.request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                tokenized_mail_message = self.send_tokenized_mail(email)
                return JsonResponse({'success': True, 'message': tokenized_mail_message},
                                    status=200)
            else:
                errors = json.loads(json.dumps(form.errors))
                return JsonResponse({'errors': errors}, status=400)
        return redirect('welcome-page')


class ConfirmEmailAndRegister(TokenMixin,
                              View):
    token_type = TokenTypes.SIGNUP

    def get(self, *args, **kwargs):
        form = SignUpForm()
        email = kwargs.pop('email')
        token = kwargs.pop('token')

        context = {
            'email': email,
            'form': form,
        }
        token_data = get_token_data(token, email)
        if token_data.error:
            context['token_error'] = token_data.error
        return render(self.request, template_name='users/signup.html', context=context)

    def post(self, *args, **kwargs):
        email = kwargs.pop('email')
        token = kwargs.pop('token')
        form = SignUpForm(self.request.POST)
        context = {
            'email': email,
            'form': form,
        }
        token_data = get_token_data(token, email)
        if form.is_valid() and token_data.token:
            user = form.save(commit=False)
            user.email = email
            user.username = User.objects.generate_username(email)
            user.save()
            login(self.request, user, backend=DEFAULT_AUTH)
            token_data.token.delete()
        else:
            print(form.errors)
            return render(self.request, template_name='users/signup.html', context=context)
        return redirect('welcome-page')


class SignIn(View):

    def post(self, *args, **kwargs):
        if is_ajax(self.request):
            form = SignInForm(self.request.POST)
            if form.is_valid():
                user = User.objects.get(email=form.cleaned_data['email'])
                login(self.request, user, backend=DEFAULT_AUTH)
                return JsonResponse({'success': True}, status=200)
            else:
                errors = json.loads(json.dumps(form.errors))
                return JsonResponse({'errors': errors}, status=400)
        return redirect('welcome-page')
