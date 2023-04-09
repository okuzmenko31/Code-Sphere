from .forms import SignUpEmailForm, SignInForm


def auth_forms(request):
    context = {
        'signup_form': SignUpEmailForm(),
        'signin_form': SignInForm()
    }
    return context
