import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import SignUpEmailForm, SignUpForm
from django.views import View
from .models import User
from .utils import ConfirmationTokenMixin, ConfirmationMailMixin


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class ConfirmEmailAndRegister(ConfirmationTokenMixin, View):

    def get(self, *args, **kwargs):
        form = SignUpForm()
        email = kwargs.pop('email')
        token = kwargs.pop('token')

        context = {
            'email': email,
            'form': form,
        }
        token_error_context = self.check_token(token, email)
        if token_error_context is not None:
            context.update(token_error_context)
        return render(self.request, template_name='users/signup.html', context=context)

    def post(self, *args, **kwargs):
        email = kwargs.pop('email')
        token = kwargs.pop('token')
        form = SignUpForm(self.request.POST)
        context = {
            'email': email,
            'form': form,
        }
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email
            user.username = User.objects.generate_username(email)
            user.save()
            self.delete_token(token=token, email=user.email)
        else:
            print(form.errors)
            return render(self.request, template_name='users/signup.html', context=context)
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
