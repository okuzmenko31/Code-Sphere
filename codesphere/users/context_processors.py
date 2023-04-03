from .forms import SignUpEmailForm


def auth_forms(request):
    context = {
        'signup_form': SignUpEmailForm()
    }
    return context
