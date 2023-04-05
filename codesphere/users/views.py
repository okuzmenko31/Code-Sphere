import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import SignUpEmailForm, SignUpForm
from django.views import View
from .models import User


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class ConfirmEmailAndRegister(View):

    def get(self, *args, **kwargs):
        email = kwargs.pop('email')
        form = SignUpForm()
        context = {
            'email': email,
            'form': form
        }
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


class SubmitRegistrationEmail(View):

    def post(self, *args, **kwargs):
        if is_ajax(self.request):
            form = SignUpEmailForm(self.request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                subject = 'Email confirmation and registration'
                html_message_template = 'users/html_email_submit_message.html'
                cont = {
                    'email': str(email),
                    'domain': '127.0.0.1:8000',
                    'site_name': 'CodeSphere',
                    'uid': urlsafe_base64_encode(force_bytes(email)),
                    'protocol': 'https' if self.request.is_secure() else 'http'
                }
                mail_message = render_to_string(html_message_template, cont)
                send_mail(subject, 'confirm', settings.EMAIL_HOST_USER, [email], html_message=mail_message)
                success_message = 'Mail was send to your email. Please check it, confirm email and register'
                return JsonResponse({'success': True, 'message': success_message}, status=200)
            else:
                errors = json.loads(json.dumps(form.errors))
                return JsonResponse({'errors': errors}, status=400)
        return redirect('welcome-page')
