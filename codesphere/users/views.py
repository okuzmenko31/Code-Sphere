import json
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import SignUpEmailForm, SignUpForm
from django.views import View
from .models import User, Token
from .utils import ConfirmationTokenMixin, ConfirmationMailMixin


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class ConfirmEmailAndRegister(ConfirmationTokenMixin, View):

    def get(self, *args, **kwargs):
        email = kwargs.pop('email')
        token_from_url = kwargs.pop('token')
        form = SignUpForm()

        context = {
            'email': email,
            'form': form,
        }

        try:
            encoded_token = force_str(urlsafe_base64_decode(token_from_url))
            token = Token.objects.get(token=encoded_token, owner_email=email)
            if token.expired:
                context['token_error'] = self.get_token_expired_error()
        except (Exception,):
            context['token_error'] = self.get_token_miss_error()
        return render(self.request, template_name='users/signup.html', context=context)

    def post(self, *args, **kwargs):
        email = kwargs.pop('email')
        form = SignUpForm(self.request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email
            user.username = User.objects.generate_username(email)
            user.save()
        else:
            return render(self.request, 'users/signup.html', {'form': form, 'email': email})
        return redirect('welcome-page')


class SubmitRegistrationEmail(ConfirmationTokenMixin,
                              ConfirmationMailMixin,
                              View):
    html_message_template = 'users/mails/registration_mail.html'
    token_type = 'su'

    def post(self, *args, **kwargs):
        if is_ajax(self.request):
            form = SignUpEmailForm(self.request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                self.token_owner = email
                self.send_confirmation_mail(self.request, email, self.token_type, self.get_token())
                success_message = self.get_success_message(self.token_type)
                return JsonResponse({'success': True, 'message': success_message}, status=200)
            else:
                errors = json.loads(json.dumps(form.errors))
                return JsonResponse({'errors': errors}, status=400)
        return redirect('welcome-page')
